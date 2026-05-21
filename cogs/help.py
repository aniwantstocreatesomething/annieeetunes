# cogs/help.py
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def help_command(self, ctx, *, command_name: str = None):
        """Bot ke saare commands ki list ya kisi specific command ki detail dikhata hai."""
        
        prefix = ctx.prefix

        # ---- CASE 1: Agar user ne sirf !help ya !!help likha hai ----
        if not command_name:
            embed = discord.Embed(
                title=f"🤖 {self.bot.user.name} Help Menu",
                description=f"Mera prefix **`{prefix}`** hai. Kisi command ki detail dekhne ke liye `{prefix}help <command>` likhein.",
                color=discord.Color.blue()
            )
            
            # --- 👑 OWNER ONLY CATEGORY ---
            if await self.bot.is_owner(ctx.author):
                embed.add_field(name="👑 Owner Only", value="`servers`, `sync`, `setstatus`", inline=False)
            
            # --- 🛡️ MODERATION CATEGORY (Ekdum Sahi Sequence Me Fixed!) ---
            # Sequence: warn, warnings, delwarn, clearwarn, mute, unmute, kick, ban, unban, purge, slowmode, lock, unlock, lockdown, say
            mod_list = "`warn`, `warnings`, `delwarn`, `clearwarn`, `mute`, `unmute`, `kick`, `ban`, `unban`, `purge`, `slowmode`, `lock`, `unlock`, `lockdown`, `say`"
            embed.add_field(name="🛡️ Moderation", value=mod_list, inline=False)
            
            # --- ⚙️ UTILITY CATEGORY ---
            util_list = "`serverinfo`, `botinfo`, `invite`"
            embed.add_field(name="⚙️ Utility", value=util_list, inline=False)
            
            # --- ✨ GENERAL CATEGORY ---
            general_list = "`afk`"
            embed.add_field(name="✨ General", value=general_list, inline=False)

            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            return await ctx.send(embed=embed)

        # ---- CASE 2: Agar user ne !help <command> likha hai ----
        cmd = self.bot.get_command(command_name.lower())

        if not cmd:
            return await ctx.send(f"❌ Mujhe `{command_name}` naam ka koi command nahi mila!")

        # Custom logic for hidden owner checking
        if cmd.name in ["servers", "sync"] and not await self.bot.is_owner(ctx.author):
            return await ctx.send("❌ Aapke paas is command ki details dekhne ki permission nahi hai!")

        description = "Koi description nahi di gayi."
        usage = f"`{prefix}{cmd.name}`"
        aliases = ", ".join([f"`{a}`" for a in cmd.aliases]) if cmd.aliases else "Koi alias nahi hai."
        examples = f"`{prefix}{cmd.name}`"
        
        # Category Mapping for Embed Detail
        if cmd.name in ["servers", "sync", "setstatus"]:
            category = "Owner Only"
        elif cmd.name in ["warn", "warnings", "delwarn", "clearwarn", "mute", "unmute", "kick", "ban", "unban", "purge", "slowmode", "lock", "unlock", "lockdown", "say"]:
            category = "Moderation"
        elif cmd.name in ["serverinfo", "botinfo", "invite"]:
            category = "Utility"
        else:
            category = "General"

        # Commands ki custom details (SAY command added and fixed below!)
        if cmd.name == "setstatus":
            description = "Bot ka status aur activity badalne ke liye."
            usage = f"**Basic:** `{prefix}setstatus <status>`\n**Advanced:** `{prefix}setstatus <status> <playing/watching/listening> <text>`"
            examples = f"`{prefix}setstatus dnd`\n`{prefix}setstatus online watching anime`"
        elif cmd.name == "warn":
            description = "Kisi member ko officially warn karne ke liye aur unke DM me message bhejne ke liye."
            usage = f"`{prefix}warn @user <reason>`"
            examples = f"`{prefix}warn @User Playing Odd Songs`"
        elif cmd.name == "warnings":
            description = "Kisi member ki purani saari warnings ki list dekhne ke liye."
            usage = f"`{prefix}warnings @user`"
            examples = f"`{prefix}warnings @User`"
        elif cmd.name == "delwarn":
            description = "Kisi user ki koi ek specific warning number delete karne ke liye."
            usage = f"`{prefix}delwarn @user <warning_number>`"
            examples = f"`{prefix}delwarn @User 1` -> Pehli warning delete karega."
        elif cmd.name == "clearwarn":
            description = "Kisi member ki saari warnings ek baar me poori tarah saaf karne ke liye."
            usage = f"`{prefix}clearwarn @user`"
            examples = f"`{prefix}clearwarn @User`"
        elif cmd.name == "mute":
            description = "Kisi member ko specific samay (seconds, minutes, hours, days) ke liye timeout (mute) karne ke liye."
            usage = f"`{prefix}mute @user <duration><s/m/h/d> <reason>`"
            examples = f"`{prefix}mute @User 10m Abusing` -> 10 minutes ke liye."
        elif cmd.name == "unmute":
            description = "Kisi member ka timeout samay se pehle hatane ke liye."
            usage = f"`{prefix}unmute @user <reason>`"
            examples = f"`{prefix}unmute @User Galti se mute hua`"
        elif cmd.name == "invite":
            description = "Bot ko apne khud ke kisi server me add karne ke liye official invite link nikalne ke liye."
            usage = f"`{prefix}invite`"
            examples = f"`{prefix}invite`"
        elif cmd.name == "serverinfo":
            description = "Jis server me aap hain uski poori details (Owner, Staff Roles aur Member counts) dekhne ke liye."
            usage = f"`{prefix}serverinfo`"
            examples = f"`{prefix}serverinfo`"
        elif cmd.name == "botinfo":
            description = "Bot ki live statistics (Total servers, monitored members aur tech specs) dekhne ke liye."
            usage = f"`{prefix}botinfo`"
            examples = f"`{prefix}botinfo`"
        elif cmd.name == "afk":
            description = "Aapko AFK status par dalne ke liye taaki jab koi aapko ping kare toh bot use reason bataye."
            usage = f"`{prefix}afk <reason>`"
            examples = f"`{prefix}afk Khana kha raha hu`"
        elif cmd.name == "purge":
            description = "Chat se normal messages, sirf bots ke messages, ya kisi specific user ke messages filter karke delete karne ke liye."
            usage = f"`{prefix}purge <amount>`\n`{prefix}purge bots <amount>`\n`{prefix}purge @user <amount>`"
            examples = f"`{prefix}purge 20` -> 20 normal msgs.\n`{prefix}purge bots 50` -> 50 me se sirf bots ke msgs."
        elif cmd.name == "kick":
            description = "Kisi member ko server ke rules todne par server se bahar nikalne ke liye."
            usage = f"`{prefix}kick @user <reason>`"
            examples = f"`{prefix}kick @User Misbehave`"
        elif cmd.name == "ban":
            description = "Kisi member ko server se permanent ban karne ke liye."
            usage = f"`{prefix}ban @user <reason>`"
            examples = f"`{prefix}ban @User Scam Link Sharing`"
        elif cmd.name == "unban":
            description = "Kisi banned user ka ban hatakar use server me wapas aane ki permission dene ke liye."
            usage = f"`{prefix}unban <User_ID>`"
            examples = f"`{prefix}unban 727718500663033897`"
        elif cmd.name == "servers":
            description = "Sirf Bot Creator ke liye! Bot jin-jin servers me add hai, unki poori list aur owner ka naam dekhne ke liye."
            usage = f"`{prefix}servers`"
            examples = f"`{prefix}servers`"
        elif cmd.name == "slowmode":
            description = "Channel cooldown rate set karne ke liye taaki log ruk kar chat karein."
            usage = f"`{prefix}slowmode <seconds>`"
            examples = f"`{prefix}slowmode 10` -> 10s cooldown.\n`{prefix}slowmode 0` -> Slowmode OFF."
        elif cmd.name == "lock":
            description = "Channel ko explicit timer aur reason ke saath lock karne ke liye."
            usage = f"`{prefix}lock [#channel] [time] [reason]`"
            examples = f"`{prefix}lock #general 30m Spamming!`\n`{prefix}lock` -> Current channel permanently freeze."
        elif cmd.name == "unlock":
            description = "Kisi locked channel ko wapas open karne ke liye."
            usage = f"`{prefix}unlock [#channel]`"
            examples = f"`{prefix}unlock #general`"
        elif cmd.name == "lockdown":
            description = "🚨 EMERGENCY COMMAND: Poore server ke saare text channels ko ek baar me lock/unlock karne ke liye."
            usage = f"`{prefix}lockdown` -> Lockdown chalu.\n`{prefix}lockdown off` -> Lockdown hatane ke liye."
            examples = f"`{prefix}lockdown`\n`{prefix}lockdown off`"
        elif cmd.name == "say":
            description = "📢 Bot ke zariye chat me apni marzi ka message bhejne ya kisi user ko target karke ping karwane ke liye."
            usage = f"`{prefix}say <message>`\n`{prefix}say @user <message>`"
            examples = f"`{prefix}say Hello Rishav~`\n`{prefix}say @User Idhar aao jaldi`"

        cmd_embed = discord.Embed(title=f"ℹ️ Command Detail: {cmd.name.upper()}", color=discord.Color.green())
        cmd_embed.add_field(name="📝 Description", value=description, inline=False)
        cmd_embed.add_field(name="⌨️ Usage", value=usage, inline=False)
        
        # SAbhi commands ke liye ab examples filter on hai
        cmd_embed.add_field(name="💡 Examples", value=examples, inline=False)
            
        cmd_embed.add_field(name="🔀 Aliases (Shortforms)", value=aliases, inline=False)
        cmd_embed.add_field(name="📁 Category", value=category, inline=True)

        await ctx.send(embed=cmd_embed)

async def setup(bot):
    await bot.add_cog(Help(bot))