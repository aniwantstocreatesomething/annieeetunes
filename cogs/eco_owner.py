# cogs/eco_owner.py
import discord
from discord.ext import commands
import sqlite3

class EcoOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"

    async def fetch_user(self, ctx, user_str):
        # Pehle Member tag check karo, fir direct ID string
        try:
            member = await commands.MemberConverter().convert(ctx, user_str)
            return str(member.id), member.name
        except Exception:
            try:
                user = await self.bot.fetch_user(int(user_str))
                return str(user.id), user.name
            except Exception:
                return None, None

    @commands.command(name="add-money", aliases=["addmoney"], hidden=True)
    @commands.is_owner()
    async def add_money(self, ctx, user_str: str = None, amount: int = None):
        """Sirf Rishav bhai ke liye - Kisi ke bhi wallet me globally paise add karne ke liye."""
        if not user_str or amount is None:
            return await ctx.send(f"❌ Sahi tarika: `{ctx.prefix}add-money @user/ID <amount>`")

        user_id, username = await self.fetch_user(ctx, user_str)
        if not user_id:
            return await ctx.send("❌ User nahi mila! Sahi tag ya valid ID daalein.")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (user_id,))
        cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        conn.close()

        await ctx.send(f"👑 **Owner Action:** Kamyabi se **{username}** (ID: `{user_id}`) ke wallet me 🪙 `{amount:,}` coins add kar diye gaye!")

    @commands.command(name="reset-money", aliases=["resetmoney"], hidden=True)
    @commands.is_owner()
    async def reset_money(self, ctx, user_str: str = None):
        """Sirf Rishav bhai ke liye - Kisi ka bhi pura bank aur wallet 0 karne ke liye."""
        if not user_str:
            return await ctx.send(f"❌ Sahi tarika: `{ctx.prefix}reset-money @user/ID`")

        user_id, username = await self.fetch_user(ctx, user_str)
        if not user_id:
            return await ctx.send("❌ User nahi mila!")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO economy (user_id, wallet, bank) VALUES (?, 0, 0)", (user_id,))
        cursor.execute("UPDATE economy SET wallet = 0, bank = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

        await ctx.send(f"👑 **Owner Action:** **{username}** (ID: `{user_id}`) ka pura bahi-khata globally **RESET (0)** kar diya gaya hai!")

async def setup(bot):
    await bot.add_cog(EcoOwner(bot))