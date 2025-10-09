import discord
from discord.ext import commands
from discord import app_commands

class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="意見箱", description="給這個群組意見")
    @app_commands.describe(name="你是誰", opinion="輸入意見")
    async def commit(self, interaction: discord.Interaction, name: str, opinion: str):
        owner = await self.bot.fetch_user(277692370622087168)  # 請填入你自己的 Discord ID
        try:
            await owner.send(f"{name} {opinion}")
            await interaction.response.send_message("意見已送出！", ephemeral=True)
        except:
            await interaction.response.send_message("找不到頻道，請聯絡管理員。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Feedback(bot))
