# cogs/music_dj.py
import discord
from discord.ext import commands
import sqlite3

class MusicDJ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    @commands.command(name="setdj")
    @commands.has_permissions(manage_guild=True)
    async def setdj(self, ctx, role: discord.Role = None):
        """Server ka custom DJ role set karne ke liye (Manage Server perms)."""
        if not role:
            return await ctx.send(f"❌ Sahi tarika: `{ctx.prefix}setdj @Role ya Role_ID`")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO dj_roles (server_id, role_id) VALUES (?, ?)", (str(ctx.guild.id), str(role.id)))
        conn.commit()
        conn.close()

        await ctx.send(f"🎧 **DJ Setup:** Successfully {role.mention} ko server ka official DJ role set kar diya gaya hai!")

async def setup(bot):
    await bot.add_cog(MusicDJ(bot))