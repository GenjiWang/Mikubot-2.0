import discord
from discord.ext import commands
from discord import app_commands
import requests
import asyncio
import io
import json
from random import randint
import time

class comfy_AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @app_commands.command(name="畫圖", description="讓初音畫圖")
    @app_commands.describe(prompt="你想畫什麼？")
    async def draw(self, interaction: discord.Interaction, prompt: str):
        user_id = interaction.user.id
        now = time.time()

        # 檢查冷卻
        if user_id in self.cooldowns and now - self.cooldowns[user_id] < 300:
            remain = int(300 - (now - self.cooldowns[user_id]))
            await interaction.response.send_message(f"⏳ 請等 {remain} 秒再使用這個指令", ephemeral=True)
            return

        # 記錄使用時間
        self.cooldowns[user_id] = now
        await interaction.response.send_message(f"🎨 正在生成：{prompt}")
        if prompt.strip() == "":
            await interaction.followup.send("❗ 請輸入有效的提示詞")
            return

        # 1. 載入 workflow
        with open(r"E:\DiscordBot\DiscordBot_workflow.json", "r", encoding="utf-8") as f:
            prompt_graph = json.load(f)

        # 修改正面提示詞 (id=13 的 CLIPTextEncode)
        prompt_graph["13"]["inputs"]["text"] = prompt
        prompt_graph["8"]["inputs"]["seed"] =randint(0,(2**32)-1)

        # 2. 發送到 ComfyUI
        try:
            r = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": prompt_graph})
            r.raise_for_status()
            task_id = r.json()["prompt_id"]
        except Exception as e:
            await interaction.followup.send(f"❌ 無法連線到 ComfyUI：{e}")
            return

        # 3. 輪詢結果（最多等 2 分鐘）
        result = None
        for _ in range(60):
            try:
                res = requests.get(f"http://127.0.0.1:8188/history/{task_id}")
                data = res.json()
                if task_id in data:
                    result = data[task_id]
                    break
            except Exception:
                pass
            await asyncio.sleep(2)

        if result is None:
            await interaction.followup.send("⚠️ 圖片生成超時，請稍後再試")
            return

        # 4. 解析輸出圖片資訊
        filename = None
        subfolder = None
        for node_id, output in result.get("outputs", {}).items():
            if "images" in output:
                filename = output["images"][0]["filename"]
                subfolder = output["images"][0]["subfolder"]
                break

        if not filename:
            await interaction.followup.send("❌ 沒有生成圖片")
            return

        # 5. 下載圖片
        url = f"http://127.0.0.1:8188/api/view?filename={filename}&type=temp&subfolder="
        print(url)
        try:
            image_data = requests.get(url).content
            file = discord.File(io.BytesIO(image_data), filename="result.png")
            await interaction.followup.send(file=file)
        except Exception as e:
            await interaction.followup.send(f"❌ 圖片下載失敗：{e}")


async def setup(bot):
    await bot.add_cog(comfy_AI(bot))