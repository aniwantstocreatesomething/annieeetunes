import discord
from discord.ext import commands
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        start_time = time.time()
        
        # Calculate bot latency
        latency = round(self.bot.latency * 1000)
        
        # Create embed initially
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Bot Latency:** `{latency}ms`\n**API Latency:** `Calculating...`",
            color=discord.Color.green()
        )
        message = await ctx.send(embed=embed)
        
        # Calculate API latency
        end_time = time.time()
        api_latency = round((end_time - start_time) * 1000)
        
        # Update embed
        embed.description = f"**Bot Latency:** `{latency}ms`\n**API Latency:** `{api_latency}ms`"
        await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
