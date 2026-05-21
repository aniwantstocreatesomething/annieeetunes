# cogs/eco_rob.py
import discord
from discord.ext import commands
import sqlite3
import random

class EcoRob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    def get_wallet(self, cursor, user_id: str):
        cursor.execute("SELECT wallet FROM economy WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (user_id,))
            return 0
        return row[0]

    @commands.cooldown(1, 1800, commands.BucketType.user)
    @commands.command(name="rob", aliases=["steal"])
    async def rob(self, ctx, member: discord.Member = None):
        """Kisi user ke wallet se cash churaane ke liye."""
        if member is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("❌ Bhai, kisko lootna hai? Tag toh karo! `!!rob @user`")
            
        if member.id == ctx.author.id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("❌ Apne aap ko lootoge toh psychiatric ward bhejna padega!")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Balance setup check
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (str(ctx.author.id),))
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (str(member.id),))
        
        author_wallet = self.get_wallet(cursor, str(ctx.author.id))
        target_wallet = self.get_wallet(cursor, str(member.id))

        if target_wallet < 200:
            ctx.command.reset_cooldown(ctx)
            conn.close()
            return await ctx.send(f"❌ {member.mention} bechara gareeb hai, uske pocket me kam se kam 200 coins toh rehne do!")

        success_chance = 40
        if target_wallet > (author_wallet * 2) and author_wallet > 0:
            success_chance = 25 

        roll = random.randint(1, 100)

        if roll <= success_chance:
            loot_percent = random.randint(20, 60)
            stolen_amount = int(target_wallet * (loot_percent / 100))
            
            cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE user_id = ?", (stolen_amount, str(member.id)))
            cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (stolen_amount, str(ctx.author.id)))
            await ctx.send(f"🥷💰 **Loot Liya!** {ctx.author.mention} ne {member.mention} ke pocket se 🪙 `{stolen_amount}` coins udaye! 🏃‍♂️💨")
        else:
            fine_amount = random.randint(100, 300)
            actual_fine = min(fine_amount, author_wallet) if author_wallet > 0 else 0
            
            if actual_fine > 0:
                cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE user_id = ?", (actual_fine, str(ctx.author.id)))
                cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (actual_fine, str(member.id)))
                await ctx.send(f"❌ **Pakde gaye!** Fine ke roop me 🪙 `{actual_fine}` coins aapke wallet se katkar {member.mention} ko de diye gaye!")
            else:
                await ctx.send(f"❌ **Pakde gaye!** Wallet khali tha isliye target ne aapko do mukke maar kar chhoda! 🥊")

        conn.commit()
        conn.close()

    @rob.error
    async def eco_errors(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Thoda sabr rakh bhai! Coodown chal raha hai. **{int(error.retry_after)} seconds** baad try karna.")

async def setup(bot):
    await bot.add_cog(EcoRob(bot))