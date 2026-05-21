# cogs/music_seek.py
import discord
from discord.ext import commands
import wavelink

class MusicSeek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seek")
    async def seek(self, ctx, time_str: str = None):
        """Gaane ko track pe aage-piche khichne ke liye (Example: !!seek 1m30s ya 45s)."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or not vc.track:
            return await ctx.send("❌ Abhi koi gaana chal hi nahi raha hai!")

        if not time_str:
            return await ctx.send("❌ Kitna aage badhana hai batao! Format: `1m30s` ya `40s`")

        # Basic parser for time string conversion to milliseconds
        seconds = 0
        try:
            if 'm' in time_str:
                parts = time_str.split('m')
                minutes = int(parts[0])
                seconds += minutes * 60
                if parts[1] and 's' in parts[1]:
                    seconds += int(parts[1].replace('s', ''))
            else:
                seconds += int(time_str.replace('s', ''))
        except Exception:
            return await ctx.send("❌ Galat format! Sahi use: `!!seek 1m20s` ya `!!seek 15s`")

        ms = seconds * 1000
        if ms > vc.track.length:
            return await ctx.send("❌ Utna lamba toh gaana hi nahi hai bhai!")

        await vc.seek(ms)
        await ctx.send(f"⏩ **Track Seeked:** Gaana **{time_str}** par set kar diya gya hai.")

async def setup(bot):
    await bot.add_cog(MusicSeek(bot))