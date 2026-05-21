# cogs/music_search.py
import discord
from discord.ext import commands
import wavelink
import asyncio

class MusicSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="search")
    async def search(self, ctx, *, query: str = None):
        """Top 10 matches search karke channe ka option deta hai."""
        if not query:
            return await ctx.send("❌ Kya dhoondhna hai likho toh sahi!")

        if not ctx.author.voice:
            return await ctx.send("❌ Pehle voice channel me aao bhai!")

        await ctx.send(f"🔎 **Top 10 search items dhoondh raha hu for:** `{query}`...")
        
        try:
            tracks = await wavelink.YouTubeTrack.search(query)
            if not tracks:
                return await ctx.send("❌ Koi matches nahi mile!")

            # Slice top 10 results
            top_tracks = tracks[:10]
            search_text = ""
            for i, t in enumerate(top_tracks, start=1):
                search_text += f"**{i}.** {t.title} (`{int(t.length//60)}m`)\n"

            embed = discord.Embed(title="🎵 Search Results Selector", description=search_text + "\n👉 **Agli 30s me bas index number (1-10) chat me type kijiye play karne ke liye!**", color=discord.Color.gold())
            menu_msg = await ctx.send(embed=embed)

            def check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.isdigit()

            try:
                response = await self.bot.wait_for("message", check=check, timeout=30.0)
                index = int(response.content) - 1
                
                if index < 0 or index >= len(top_tracks):
                    return await ctx.send("❌ Galat index number chuna aapne! Cancelled.")

                selected_track = top_tracks[index]
                
                # Setup player
                if not ctx.voice_client:
                    vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
                else:
                    vc = ctx.voice_client

                if vc.is_playing():
                    await vc.queue.put(selected_track)
                    await ctx.send(f"➕ **Queue me joda:** `{selected_track.title}`")
                else:
                    await vc.play(selected_track)
                    await ctx.send(f"▶️ **Playing Selected:** `{selected_track.title}`")

            except asyncio.TimeoutError:
                await menu_msg.edit(content="⏱️ Timeout! Aapne selection me bohot der kardi.", embed=None)

        except Exception as e:
            await ctx.send("❌ Search engine temporary heavy load par hai!")

async def setup(bot):
    await bot.add_cog(MusicSearch(bot))