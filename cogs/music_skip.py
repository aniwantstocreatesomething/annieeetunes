# cogs/music_skip.py
import discord
from discord.ext import commands
import sqlite3
import wavelink

class MusicSkip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "warnings.db"
        self.votes = {} # Structure: {channel_id: set(user_ids)}

    def has_dj(self, member):
        # Admin perms ya custom role check logic
        if member.guild_permissions.manage_guild:
            return True
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM dj_roles WHERE server_id = ?", (str(member.guild.id),))
        row = cursor.fetchone()
        conn.close()
        if row:
            role_id = int(row[0])
            if discord.utils.get(member.roles, id=role_id):
                return True
        return False

    async def do_skip(self, ctx, vc):
        if vc.queue.is_empty:
            await vc.stop()
            await ctx.send("⏹️ Queue khali thi, player rok diya gya!")
        else:
            next_track = vc.queue.get()
            await vc.play(next_track)
            await ctx.send(f"⏭️ **Skipped!** Ab chal raha hai: `{next_track.title}`")

    @commands.command(name="skip", aliases=["s", "forceskip", "fs"])
    async def skip(self, ctx):
        """Gaana skip karne ke liye (DJ instant / Normal members voting)."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or not vc.is_playing():
            return await ctx.send("❌ Abhi koi gaana chal hi nahi raha hai!")

        # Listeners count (Bot ko count nahi karenge)
        listeners = len([m for m in ctx.author.voice.channel.members if not m.bot])
        
        # Condition 1: Direct forceskip via DJ perms, alias input, ya single listener
        if self.has_dj(ctx.author) or ctx.invoked_with in ["forceskip", "fs"] or listeners <= 1:
            if ctx.invoked_with in ["forceskip", "fs"] and not self.has_dj(ctx.author):
                return await ctx.send("❌ Forceskip sirf DJ role ya Admin hi kar sakte hain!")
            
            self.votes[ctx.channel.id] = set() # Reset votes
            await ctx.send("⚡ **DJ/Force Skip:** Immediate skip execute kiya gaya!")
            return await self.do_skip(ctx, vc)

        # Condition 2: Voting System for Regular Members
        if ctx.channel.id not in self.votes:
            self.votes[ctx.channel.id] = set()

        if ctx.author.id in self.votes[ctx.channel.id]:
            return await ctx.send("❌ Aapne pehle hi vote de diya hai bhai!")

        self.votes[ctx.channel.id].add(ctx.author.id)
        current_votes = len(self.votes[ctx.channel.id])
        required_votes = int(listeners / 2) + 1 if listeners % 2 == 0 else int(listeners // 2) + 1

        if current_votes >= required_votes:
            self.votes[ctx.channel.id] = set() # Clear votes
            await ctx.send(f"🎉 **Vote Passed!** ({current_votes}/{listeners} Votes). Skipping...")
            await self.do_skip(ctx, vc)
        else:
            await ctx.send(f"🗳️ **Skip Vote:** {ctx.author.mention} ne skip ke liye vote kiya! ({current_votes}/{required_votes} votes required).")

async def setup(bot):
    await bot.add_cog(MusicSkip(bot))