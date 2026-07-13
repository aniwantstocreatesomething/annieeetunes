import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Default system channel or a channel named 'welcome'
        channel = member.guild.system_channel
        if not channel:
            channel = discord.utils.get(member.guild.text_channels, name='welcome')
        
        if channel:
            embed = discord.Embed(
                title="Welcome to the Dev Server!",
                description=f"Hey {member.mention}, welcome to **{member.guild.name}**! 🚀\nMake sure to read the rules and enjoy your stay.",
                color=discord.Color.gold()
            )
            if member.avatar:
                embed.set_thumbnail(url=member.avatar.url)
            
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
