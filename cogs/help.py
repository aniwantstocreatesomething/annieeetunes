import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🛠️ Dev Bot Help",
            description="Here are the available commands for this dev server bot. Note: Most commands require Administrator or Moderator permissions.",
            color=discord.Color.blue()
        )
        
        # Moderation Commands
        mod_desc = (
            "`$ban <user> [reason]` - Ban a user\n"
            "`$kick <user> [reason]` - Kick a user\n"
            "`$mute <user> [reason]` - Mute a user (timeout)\n"
            "`$unmute <user>` - Unmute a user\n"
            "`$warn <user> <reason>` - Warn a user\n"
            "`$warnings <user>` - View user warnings\n"
            "`$clearwarn <user>` - Clear user warnings\n"
            "`$delwarn <user> <id>` - Delete a specific warning\n"
            "`$purge <amount>` - Delete messages\n"
            "`$lock` / `$lockdown` - Lock a channel or server\n"
            "`$unlock` - Unlock a channel"
        )
        embed.add_field(name="🛡️ Moderation", value=mod_desc, inline=False)
        
        # Dev Tools & Utilities
        util_desc = (
            "`$ticket_setup` - Setup the ticket system button (Admin Only)\n"
            "`$ping` - Check bot latency\n"
            "`$eval <code>` - Evaluate Python code (Owner Only)\n"
            "`$bug <description>` - Report a bug\n"
            "`$suggest <suggestion>` - Suggest a new feature\n"
            "`$say <message>` - Make the bot say something (Admin Only)\n"
            "`$help` - Show this menu"
        )
        embed.add_field(name="⚙️ Utilities & Dev Tools", value=util_desc, inline=False)
        
        embed.set_footer(text="SpaceX Dev Bot • Built for Developers")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
