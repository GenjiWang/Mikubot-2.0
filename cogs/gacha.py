import discord
from discord.ext import commands
from discord import app_commands
from random import choices, randint
from asyncio import sleep

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='單抽神教', description='單抽YYDS')
    async def gacha1(self, interaction: discord.Interaction):
        can_get = ["4star", "3star", "2star"]
        can_get_stickers = {
            "4star": "<:4star:948514272185569330>",
            "3star": "<:3star:948514271833235486>",
            "2star": "<:2star:948514272290414622>"
        }
        gtl = choices(can_get, weights=[3, 8.5, 88.5], k=1)
        await interaction.response.send_message(f"{can_get_stickers[gtl[0]]}")

    @app_commands.command(name='來發十連', description='抽10抽世界計畫卡池')
    async def gacha10(self, interaction: discord.Interaction):
        await self._gacha_draw(interaction, [3, 8.5, 88.5])

    @app_commands.command(name='雙倍十連', description='懂不懂fes池的含金量')
    async def gacha10double(self, interaction: discord.Interaction):
        await self._gacha_draw(interaction, [6, 8.5, 85.5])

    async def _gacha_draw(self, interaction: discord.Interaction, weights):
        can_get = ["4star", "3star", "2star"]
        stickers = {
            "4star": "<:4star:948514272185569330>",
            "3star": "<:3star:948514271833235486>",
            "2star": "<:2star:948514272290414622>"
        }

        gtl = choices(can_get, weights=weights, k=10)
        if "4star" and "3star" not in gtl:
            gtl[randint(0, 9)] = choices(["4star", "3star"], weights=weights[:2])[0]

        msg = ""
        for idx, item in enumerate(gtl, 1):
            msg += stickers[item]
            if idx == 5:
                msg += "\n"

        if "4star" in gtl:
            await interaction.response.send_message(stickers["4star"])
        else:
            await interaction.response.send_message(stickers["3star"])
        await sleep(2)
        await interaction.edit_original_response(content=msg)

async def setup(bot):
    await bot.add_cog(Gacha(bot))
