# cogs/music_shuffle.py
import discord
from discord.ext import commands
import wavelink
import random

class MusicShuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        """Upcoming queue ke gaano ko shuffle mix karne ke liye."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or vc.queue.is_empty:
            return await ctx.send("❌ Shuffle karne ke liye queue me gaane toh hone chahiye!")

        # Convert queue to list, shuffle it, and clear-put it back
        track_list = []
        while not vc.queue.is_empty:
            track_list.append(vc.queue.get())
            
        random.shuffle(track_list)
        for track in track_list:
            await vc.queue.put(track)

        await ctx.send("🔀 **Queue Shuffled:** Saare upcoming tracks successfully mix-up ho gaye hain!")

async def setup(bot):
    await bot.add_cog(MusicShuffle(bot))