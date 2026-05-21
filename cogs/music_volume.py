# cogs/music_volume.py
import discord
from discord.ext import commands
import wavelink
import sqlite3

class MusicVolume(commands.Cog):
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

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx, vol: int = None):
        """Bot ka volume level badalne ke liye (DJ ONLY)."""
        if not self.is_dj(ctx.author):
            return await ctx.send("❌ Yeh strictly DJ ONLY command hai bhai!")

        vc: wavelink.Player = ctx.voice_client
        if not vc: return await ctx.send("❌ Bot voice channel me nahi hai!")

        if vol is None:
            return await ctx.send(f"🔊 Current Volume Level: **{vc.volume}%**")

        if vol < 1 or vol > 100:
            return await ctx.send("❌ Volume scale 1 se 100 ke beech honi chahiye!")

        await vc.set_volume(vol)
        await ctx.send(f"🔊 **Volume Altered:** Level set to **{vol}%** by DJ!")

async def setup(bot):
    await bot.add_cog(MusicVolume(bot))