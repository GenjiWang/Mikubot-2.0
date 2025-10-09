import discord
from discord.ext import commands, tasks
from asyncio import sleep
from time import ctime

class TimeTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_to_do.start()

    @tasks.loop(seconds=1)
    async def time_to_do(self):
        time_now = ctime().split()[3]
        if '07:00:0' in time_now:
            channel = self.bot.get_channel(1227348753426682047)
            if channel:
                await channel.send('早安')
                await channel.send('<:good_morning:948514272558874644>')
                await sleep(10)

    @time_to_do.before_loop
    async def before_time_to_do(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TimeTask(bot))
