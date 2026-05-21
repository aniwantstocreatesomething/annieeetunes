# cogs/music_controls.py
import discord
from discord.ext import commands
import wavelink

class MusicControls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Current music ko pause karne ke liye."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or not vc.is_playing():
            return await ctx.send("❌ Abhi koi music chal hi nahi raha hai!")
        
        await vc.pause()
        await ctx.send("⏸️ Music ko temporary pause kar diya gaya hai!")

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Paused music ko fir se chalu karne ke liye."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or not vc.is_paused():
            return await ctx.send("❌ Music paused nahi hai bhai!")
        
        await vc.resume()
        await ctx.send("▶️ Music wapas chalu ho gaya!")

async def setup(bot):
    await bot.add_cog(MusicControls(bot))