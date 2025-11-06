import discord
from discord.ext import commands
import requests
import json

MODEL = "deepseek-r1:latest"

class OllamaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="ask", description="呼叫 DeepSeek R1 模型並回覆結果")
    async def ask(self, interaction: discord.Interaction, prompt: str):
        # 先延遲回覆，避免超時
        await interaction.response.defer()

        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={"model": "deepseek-r1:latest", "prompt": f"請用繁體中文回答：{prompt}"},
            stream=True
        )

        answer = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    answer += data["response"]

        # 用 followup 回覆
        await interaction.followup.send(answer)


async def setup(bot: commands.Bot):
    await bot.add_cog(OllamaCog(bot))