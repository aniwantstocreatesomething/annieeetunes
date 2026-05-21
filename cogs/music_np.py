# cogs/music_np.py
import discord
from discord.ext import commands
import wavelink

class MusicNP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nowplaying", aliases=["np"])
    async def nowplaying(self, ctx):
        """Current track ka visual dynamic status track progress dekhne ke liye."""
        vc: wavelink.Player = ctx.voice_client
        if not vc or not vc.track:
            return await ctx.send("❌ Board par abhi koi track active nahi hai!")

        track = vc.track
        current_pos = vc.position
        total_len = track.length

        # Math logic to design a perfect text-based 3D visual progress line bar scale
        bar_length = 15
        progress = int((current_pos / total_len) * bar_length) if total_len > 0 else 0
        bar = "".join(["▬" if i != progress else "🔘" for i in range(bar_length)])

        # Time layout rendering conversion
        cur_time = f"{int(current_pos//60)}:{int(current_pos%60):02d}"
        tot_time = f"{int(total_len//60)}:{int(total_len%60):02d}"

        embed = discord.Embed(title="💿 Vinyl Player State Tracking", description=f"▶️ **[{track.title}]({track.uri})**", color=discord.Color.green())
        embed.add_field(name="📊 Track Progress Timeline Bar", value=f"`{cur_time}` [{bar}] `{tot_time}`", inline=False)
        if hasattr(track, 'thumbnail'): embed.set_thumbnail(url=track.thumbnail)
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MusicNP(bot))