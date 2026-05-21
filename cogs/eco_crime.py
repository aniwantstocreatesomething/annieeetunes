# cogs/eco_crime.py
import discord
from discord.ext import commands
import sqlite3
import random

class EcoCrime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    @commands.cooldown(1, 1200, commands.BucketType.user)
    @commands.command(name="crime")
    async def crime(self, ctx):
        """Bada risk, bada profit! Police fine laga sakti hai."""
        success = random.choice([True, False, False])
        amount = random.randint(500, 1500)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (str(ctx.author.id),))
        
        if success:
            reasons = [
                f"Aapne Discord ke ek bade bot ka database hack kiya aur anonymous bank se 🪙 `{amount}` loot liye!",
                f"Aapne SRM canteen se chupchaap saare burger aur cold drinks uda diye aur unhe bahar bechkar 🪙 `{amount}` kamaye!"
            ]
            cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (amount, str(ctx.author.id)))
            await ctx.send(f"🥷 **Crime Success:** {random.choice(reasons)}")
        else:
            cursor.execute("SELECT wallet FROM economy WHERE user_id = ?", (str(ctx.author.id),))
            wallet = cursor.fetchone()[0]
            fine = min(random.randint(300, 1000), wallet) if wallet > 0 else 0
            
            if fine > 0:
                cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE user_id = ?", (fine, str(ctx.author.id)))
            await ctx.send(f"🚨 **Crime Fail:** Aap SRM block me admin ka paper chori kar rahe the, Dean ne pakad liya! Fine costed you 🪙 `{fine}` coins.")
            
        conn.commit()
        conn.close()

async def setup(bot):
    await bot.add_cog(EcoCrime(bot))