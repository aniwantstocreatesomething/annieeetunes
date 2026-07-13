import discord
from discord.ext import commands

class TicketCloseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket in 5 seconds...", ephemeral=True)
        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete(reason="Ticket closed by user.")

class TicketCreateButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket_btn", emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        # Permissions: Default hidden, interaction user can view and send messages.
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        # Find a mod role if it exists
        mod_role = discord.utils.get(guild.roles, name="Moderator")
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        ticket_channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="Ticket Created",
            description=f"Welcome {interaction.user.mention}! Please describe your issue, and a staff member will be with you shortly.",
            color=discord.Color.green()
        )
        
        await ticket_channel.send(embed=embed, view=TicketCloseButton())
        await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketCreateButton())
        self.bot.add_view(TicketCloseButton())

    @commands.command(name="ticket_setup")
    @commands.has_permissions(administrator=True)
    async def ticket_setup(self, ctx):
        embed = discord.Embed(
            title="Support Tickets",
            description="Click the button below to create a support ticket.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=TicketCreateButton())

async def setup(bot):
    await bot.add_cog(Tickets(bot))
