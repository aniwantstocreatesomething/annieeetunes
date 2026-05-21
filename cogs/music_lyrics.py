# cogs/music_mode.py
import discord
from discord.ext import commands
import wavelink
import sqlite3

class MusicMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    def is_dj(self, member):
        if member.guild_permissions.manage_guild: return True
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM dj_roles WHERE server_id = ?", (str(member.guild.id),))
        row = cursor.fetchone()
        conn.close()
        return row and discord.utils.get(member.roles, id=int(row[0]))

    @commands.command(name="mode", aliases=["filter"])
    async def mode(self, ctx, filter_type: str = None):
        """Audio filters badalne ke liye: !!mode bass/lofi/reset (DJ Only)."""
        if not self.is_dj(ctx.author):
            return await ctx.send("❌ Yeh badw filter controls sirf DJ role badal sakta hai!")

        vc: wavelink.Player = ctx.voice_client
        if not vc: return await ctx.send("❌ Bot channel me active nahi hai!")

        if not filter_type:
            return await ctx.send("🎛️ **Available Audio Modes:** `bass`, `lofi`, `reset`")

        if filter_type.lower() == "bass":
            # Setting manual equalizer gains for heavy bass booster
            eq = wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(0, 0.4), (1, 0.3), (2, 0.2), (3, 0.1)]))
            await vc.set_filter(eq)
            await ctx.send("🎛️ **Audio Filter Mode Set:** 🔥 **BASS BOOSTED** active!")
            
        elif filter_type.lower() == "lofi":
            eq = wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(0, -0.1), (1, 0.1), (2, 0.2), (6, -0.2)]))
            await vc.set_filter(eq)
            await ctx.send("🎛️ **Audio Filter Mode Set:** ☁️ **LOFI VIBES** active!")
            
        elif filter_type.lower() == "reset":
            await vc.set_filter(wavelink.Filter())
            await ctx.send("🎛️ Saare audio filters hatakar audio normal kar di gayi hai.")
        else:
            await ctx.send("❌ Galat filter mode! Option available: `bass`, `lofi`, `reset`")

async def setup(bot):
    await bot.add_cog(MusicMode(bot))