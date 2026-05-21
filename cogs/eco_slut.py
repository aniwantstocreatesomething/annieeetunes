# cogs/eco_slut.py
import discord
from discord.ext import commands
import sqlite3
import random

class EcoSlut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    @commands.cooldown(1, 900, commands.BucketType.user)
    @commands.command(name="slut")
    async def slut(self, ctx):
        """Kismat ke bharose thoda risky kaam karne ke liye."""
        success = random.choice([True, True, False])
        amount = random.randint(200, 800)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (str(ctx.author.id),))
        
        if success:
            reasons = [
                f"Aapne Discord e-girls ke sath flirt kiya aur unhone khush hokar aapke wallet me 🪙 `{amount}` daal diye!",
                f"Aapne Instagram par ek cringe influencer reel banayi jo viral ho gayi! Brand sponsor se 🪙 `{amount}` mile."
            ]
            cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (amount, str(ctx.author.id)))
            await ctx.send(f"💋 **Slut Success:** {random.choice(reasons)}")
        else:
            cursor.execute("SELECT wallet FROM economy WHERE user_id = ?", (str(ctx.author.id),))
            wallet = cursor.fetchone()[0]
            fine = min(amount, wallet) if wallet > 0 else 0
            
            if fine > 0:
                cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE user_id = ?", (fine, str(ctx.author.id)))
            
            await ctx.send(f"💔 **Slut Fail:** Aap Discord par badmashi kar rahe the aur server staff ne pakad kar fine laga diya! Wallet se 🪙 `{fine}` coins gaye.")
            
        conn.commit()
        conn.close()

async def setup(bot):
    await bot.add_cog(EcoSlut(bot))