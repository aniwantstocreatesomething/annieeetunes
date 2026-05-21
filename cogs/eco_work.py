# cogs/eco_work.py
import discord
from discord.ext import commands
import sqlite3
import random

class EcoWork(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.command(name="work", aliases=["job"])
    async def work(self, ctx):
        """Mehnat karke bina kisi risk ke paise kamane ke liye."""
        earnings = random.randint(100, 500)
        
        reasons = [
            f"Aapne SRM KTR campus me first-year doston ki coding assignment complete ki aur aapko 🪙 `{earnings}` mile!",
            f"Aapne ek local shop ke liye professional video edit kiya Adobe Premiere Pro par aur unhone khush hokar 🪙 `{earnings}` diye.",
            f"Aapne stand-up comedy open mic me Anubhav Bassi jaisa solid act mara! Logo ne khush hokar upar 🪙 `{earnings}` feke.",
            f"Aapne din bhar YouTube videos ke liye thumbnails design kiye aur 🪙 `{earnings}` kamaye."
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (str(ctx.author.id),))
        cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (earnings, str(ctx.author.id)))
        conn.commit()
        conn.close()
        
        await ctx.send(f"💼 **Work Done:** {random.choice(reasons)}")

async def setup(bot):
    await bot.add_cog(EcoWork(bot))