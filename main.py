# main.py
import discord
from discord.ext import commands
import os
import sqlite3
import time

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

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

def get_prefix(bot, message):
    prefixes = ['!!']
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, intents=intents, owner_ids={OWNER_ID})
bot.remove_command('help')

@bot.event
async def on_ready():
    print("---------------------------------------")
    print(f'Mubarak ho! Bot ka naam hai: {bot.user.name}')
    
    # DATABASE SETUP
    conn = sqlite3.connect("warnings.db")
    cursor = conn.cursor()

    # 🔥 CENTRAL MODERATION LOGS TABLE
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
    
    # DJ ROLE TABLE FOR MUSIC SYSTEM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dj_roles (
        server_id TEXT PRIMARY KEY, 
        role_id TEXT
    )
    """)
    
    # 🔥 NAYA JADU: GLOBAL BLACKLIST TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blacklist (
        user_id TEXT PRIMARY KEY,
        expires_at INTEGER,
        reason TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print("-> Database Connected & All Tables (Economy + DJ + Blacklist) Ready!")
    
    print('Modules load ho rahe hain...')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'-> Successfully Loaded: {filename}')
            
    print('Bot successfully online aa gaya hai! 🎉')
    print("---------------------------------------")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 🔥 CHAT CHECKER: Blacklist check karne ke liye
    current_time = int(time.time())
    conn = sqlite3.connect("warnings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT expires_at, reason FROM blacklist WHERE user_id = ?", (str(message.author.id),))
    row = cursor.fetchone()
    conn.close()

    if row:
        expires_at, reason = row[0], row[1]
        
        # Agar permanent block hai (-1) ya time bacha hai
        if expires_at == -1 or current_time < expires_at:
            # Agar blacklisted user khud !!blacklist chalaye, toh message aage jaane do (taki troll dialog chale)
            if message.content.startswith("!!blacklist") or message.content.startswith("!!bl"):
                pass
            else:
                # Baki saare commands silently block ho jayenge
                return

        # Agar blacklist ka time khatam ho gaya hai, toh database se saaf kar do
        elif current_time >= expires_at:
            conn = sqlite3.connect("warnings.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blacklist WHERE user_id = ?", (str(message.author.id),))
            conn.commit()
            conn.close()

    if bot.user.mentioned_in(message) and len(message.content.strip().split()) == 1:
        embed = discord.Embed(
            title=f"Hello {message.author.name}! 👋",
            description=f"Mera current prefix **``!!``** hai.\nAap commands ko **`!!help`** tarike se use kar sakte hain!",
            color=discord.Color.blue()
        )
        return await message.channel.send(embed=embed)

    await bot.process_commands(message)

if __name__ == '__main__':
    keep_alive()
    print("-> Background Web Server Started!")
    bot.run(BOT_TOKEN)