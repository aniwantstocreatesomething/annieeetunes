# cogs/music_play.py
import discord
from discord.ext import commands
import wavelink

class MusicPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, search: str = None):
        """YouTube/Spotify se gaana chalane ke liye."""
        if not search:
            return await ctx.send(f"❌ Sahi tarika: `{ctx.prefix}play <gaane ka naam ya link>`")

        if not ctx.author.voice:
            return await ctx.send("❌ Pehle kisi Voice Channel me aao bhai!")

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await ctx.send(f"🔍 **Searching:** `{search}`...")
        
        try:
            tracks = await wavelink.YouTubeTrack.search(search)
            if not tracks:
                return await ctx.send("❌ Koi gaana nahi mila!")
            
            track = tracks[0]
            if vc.is_playing():
                await vc.queue.put(track)
                await ctx.send(f"➕ **Queue me joda gaya:** `{track.title}`")
            else:
                await vc.play(track)
                embed = discord.Embed(title="🎵 Now Playing", description=f"▶️ **[{track.title}]({track.uri})**", color=discord.Color.blurple())
                if hasattr(track, 'thumbnail'): embed.set_thumbnail(url=track.thumbnail)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("❌ Gaana load karne me dikkat aayi. Node offline ho sakti hai!")

async def setup(bot):
    await bot.add_cog(MusicPlay(bot))