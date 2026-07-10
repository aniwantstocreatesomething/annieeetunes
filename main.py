# main.py
import discord
from discord.ext import commands
import os
import sqlite3
import time
import asyncio

# Environment Variable aur Config setup
try:
    import config
    OWNER_ID = config.OWNER_ID
    BOT_TOKEN = config.BOT_TOKEN
except ImportError:
    OWNER_ID = 727718500663033897  # Aapki asli Discord ID permanent backup
    BOT_TOKEN = os.getenv("BOT_TOKEN")

# Web Server ke liye imports (For Render 24/7)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "SpaceX Bot Is Alive & Running 24/7! 🚀"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# 🔥 GLOBAL SPEED MATRIX: Run-time Memory Cache
# Isse har message par DB fetch karne ka load 0% ho jayega
PREFIX_CACHE = {}
PREFIXLESS_CACHE = set()

# ⚙️ DYNAMIC CUSTOM PREFIX FETCH ENGINE (OPTIMIZED)
def get_prefix(bot, message):
    if not message.guild:
        return '!!'
    
    # ⚡ Cache se instantly uthao (0.000ms Latency)
    if message.guild.id in PREFIX_CACHE:
        return PREFIX_CACHE[message.guild.id]
        
    return '!!'

# Discord Bot Setup
# ⚡ SPEED HACK: Intents parsing ko explicitly direct reference access diya
intents = discord.Intents.all() 

bot = commands.Bot(command_prefix=get_prefix, intents=intents, owner_ids={OWNER_ID})
bot.remove_command('help')

# 🔥 MAINTENANCE GLOBALS
bot.maintenance_mode = False
bot.maintenance_end = 0
bot.interrupted_users = {} # Format: {user_id: channel_id}

@bot.event
async def on_ready():
    print("---------------------------------------")
    print(f'Mubarak ho! Bot ka naam hai: {bot.user.name}')
    
    # ⚡ PERSISTENT CONNECTION MATRIX
    # Bot runtime me ab sirf ek single connection object reuse karega
    bot.db = sqlite3.connect("warnings.db")
    cursor = bot.db.cursor()

    # 🔥 SQLITE PERFORMANCE PRAGMAS (Ultra-Speed Tweaks)
    cursor.execute("PRAGMA journal_mode=WAL;")  # Write-Ahead Logging for concurrency
    cursor.execute("PRAGMA synchronous=NORMAL;") # Fast disk writing bounds
    cursor.execute("PRAGMA cache_size=-64000;")  # 64MB cache optimization memory allocation

    # SERVER CUSTOM PREFIX TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS server_prefixes (
        server_id TEXT PRIMARY KEY,
        prefix TEXT
    )
    """)

    # CENTRAL MODERATION LOGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mod_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id TEXT,
        user_id TEXT,
        action TEXT,
        moderator_id TEXT,
        reason TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Moderation & AFK Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id TEXT,
        user_id TEXT,
        reason TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS afk (
        server_id TEXT,
        user_id TEXT,
        reason TEXT,
        timestamp INTEGER,
        PRIMARY KEY (server_id, user_id)
    )
    """)
    
    # GLOBAL ECONOMY TABLE (OwO Style)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS economy (
        user_id TEXT PRIMARY KEY,
        wallet INTEGER DEFAULT 0,
        bank INTEGER DEFAULT 0
    )
    """)
    
    # GLOBAL BLACKLIST TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blacklist (
        user_id TEXT PRIMARY KEY,
        expires_at INTEGER,
        reason TEXT
    )
    """)

    # PREFIXLESS USERS LEAF MATRIX TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prefixless_users (
        user_id TEXT PRIMARY KEY
    )
    """)
    
    bot.db.commit()
    
    # 🧠 WARM UP CACHE ENGINE: Memory hydration on startup
    print("-> Hydrating runtime memory cache arrays...")
    
    cursor.execute("SELECT server_id, prefix FROM server_prefixes")
    for s_id, pref in cursor.fetchall():
        PREFIX_CACHE[int(s_id)] = pref
        
    cursor.execute("SELECT user_id FROM prefixless_users")
    for (u_id,) in cursor.fetchall():
        PREFIXLESS_CACHE.add(int(u_id))
        
    print("-> Database Connected & Speed Cache Engines Synchronized!")
    
    print('Modules load ho rahe hain...')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename in ['stocks_core.py', 'eco_stocks_list.py', 'music_core.py']:
                print(f'-> Skipped Non-Cog Utility File: {filename}')
                continue
                
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'-> Successfully Loaded: {filename}')
            except Exception as e:
                print(f'💥 Failed to Load Extension {filename}: {e}')
                
    print('Bot successfully online aa gaya hai! 🎉')
    print("---------------------------------------")

def get_remaining_time_str(expires_at):
    remaining = expires_at - int(time.time())
    if remaining <= 0:
        return "kuch hi seconds"
    
    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60
    
    time_str = ""
    if hours > 0:
        time_str += f"{hours}h "
    if minutes > 0:
        time_str += f"{minutes}m "
    time_str += f"{seconds}s"
    return time_str.strip()

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    # Cache optimized fast lookup
    current_prefix = get_prefix(bot, message)

    # 🚨 STEP A: PREFIXLESS ROUTING LAYER ENGINE (FAST LOOKUP)
    is_whitelisted = False
    if message.author.id in bot.owner_ids or message.author.id in PREFIXLESS_CACHE:
        is_whitelisted = True

    # Agar banda whitelist hai aur message bina command prefix ke aaya hai
    if is_whitelisted and not message.content.startswith(current_prefix):
        tokens = message.content.split()
        if tokens:
            first_word = tokens[0].lower()
            all_commands = [cmd.name for cmd in bot.commands]
            for cmd in bot.commands:
                all_commands.extend(cmd.aliases)
            
            if first_word in all_commands:
                message.content = f"{current_prefix}" + message.content

    # 1. 🔥 MAINTENANCE SYSTEM PEHRA
    is_owner = message.author.id in bot.owner_ids
    if bot.maintenance_mode and not is_owner:
        if int(time.time()) >= bot.maintenance_end:
            bot.maintenance_mode = False
        else:
            bot.interrupted_users[message.author.id] = message.channel.id
            time_left = get_remaining_time_str(bot.maintenance_end)
            
            if message.content.startswith(current_prefix):
                embed = discord.Embed(
                    title="⚙️ Bot Under Maintenance",
                    description=f"🤖 Sorry buddy, I am under maintenance right now.\n\n⏳ **I will be back just after:** `{time_left}`",
                    color=discord.Color.red()
                )
                return await message.channel.send(embed=embed)
            return

    # 2. 🚨 GLOBAL BLACKLIST CHECKER (USES ACTIVE CONNECTION)
    current_time = int(time.time())
    cursor = bot.db.cursor()
    cursor.execute("SELECT expires_at, reason FROM blacklist WHERE user_id = ?", (str(message.author.id),))
    row = cursor.fetchone()

    if row:
        expires_at, reason = row[0], row[1]
        if expires_at == -1 or current_time < expires_at:
            if message.content.startswith(f"{current_prefix}blacklist") or message.content.startswith(f"{current_prefix}bl"):
                pass
            else:
                return
        elif current_time >= expires_at:
            cursor.execute("DELETE FROM blacklist WHERE user_id = ?", (str(message.author.id),))
            bot.db.commit()

    # Dynamic ping response handler using current prefix
    if bot.user.mentioned_in(message) and len(message.content.strip().split()) == 1:
        embed = discord.Embed(
            title=f"Hello {message.author.name}! 👋",
            description=f"Is server me mera current prefix **``{current_prefix}``** hai.\nAap commands ko **`{current_prefix}help`** tarike se use kar sakte hain!",
            color=discord.Color.blue()
        )
        return await message.channel.send(embed=embed)

    await bot.process_commands(message)

if __name__ == '__main__':
    keep_alive()
    print("-> Background Web Server Started!")
    bot.run(BOT_TOKEN)