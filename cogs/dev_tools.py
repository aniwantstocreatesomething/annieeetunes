import discord
from discord.ext import commands
import io
import textwrap
import traceback
import contextlib

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", hidden=True)
    @commands.is_owner()
    async def eval_cmd(self, ctx, *, body: str):
        """Evaluates python code (Owner Only)"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'discord': discord
        }
        env.update(globals())

        body = body.strip('` ')
        if body.startswith('py'):
            body = body[2:]

        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(name="bug")
    async def report_bug(self, ctx, *, description: str):
        """Report a bug to the developers"""
        # Look for a channel named 'bug-reports'
        channel = discord.utils.get(ctx.guild.text_channels, name='bug-reports')
        if not channel:
            return await ctx.send("The `bug-reports` channel does not exist in this server. Please ask an admin to create it.")

        embed = discord.Embed(
            title="🐛 New Bug Report",
            description=description,
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        
        await channel.send(embed=embed)
        await ctx.send("Your bug report has been submitted. Thank you!", delete_after=5)

    @commands.command(name="suggest")
    async def suggest(self, ctx, *, suggestion: str):
        """Suggest a feature"""
        channel = discord.utils.get(ctx.guild.text_channels, name='suggestions')
        if not channel:
            return await ctx.send("The `suggestions` channel does not exist in this server. Please ask an admin to create it.")

        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=discord.Color.gold()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        
        msg = await channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        
        await ctx.send("Your suggestion has been submitted. Thank you!", delete_after=5)

    @commands.command(name="say")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message: str):
        """Make the bot say something (Admin Only)"""
        await ctx.message.delete()
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(DevTools(bot))
