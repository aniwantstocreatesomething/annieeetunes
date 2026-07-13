# main.py
import discord
from discord.ext import commands
import os
import sqlite3
import asyncio

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Environment Variable aur Config setup
try:
    import config
    OWNER_ID = config.OWNER_ID
    BOT_TOKEN = config.BOT_TOKEN
except (ImportError, AttributeError):
    OWNER_ID = 727718500663033897  # Aapki asli Discord ID permanent backup
    BOT_TOKEN = os.getenv("BOT_TOKEN")

# Web Server ke liye imports (For Render 24/7)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "SpaceX Dev Bot Is Alive & Running 24/7! 🚀"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# Discord Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class SpaceXBot(commands.Bot):
    def __init__(self):
        # Prefix is now hardcoded to '$'
        super().__init__(command_prefix='$', intents=intents, owner_ids={OWNER_ID, 1061268825913438358})
        self.remove_command('help')

    async def setup_hook(self):
        # Initialize Database connection
        self.db = sqlite3.connect("warnings.db", check_same_thread=False)
        cursor = self.db.cursor()

        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")

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

        # Warnings Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT,
            user_id TEXT,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.db.commit()
        print("-> Database Connected!")
        
        print('Loading modules...')
        if os.path.exists('./cogs'):
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        await self.load_extension(f'cogs.{filename[:-3]}')
                        print(f'-> Successfully Loaded: {filename}')
                    except Exception as e:
                        print(f'💥 Failed to Load Extension {filename}: {e}')

bot = SpaceXBot()

@bot.event
async def on_ready():
    print("---------------------------------------")
    print(f'Logged in as: {bot.user.name}')
    print('Bot successfully online! 🎉')
    print("---------------------------------------")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    # Ping response
    if bot.user.mentioned_in(message) and len(message.content.strip().split()) == 1:
        embed = discord.Embed(
            title=f"Hello {message.author.name}! 👋",
            description=f"My prefix here is **`$`**.\nUse **`$help`** to see my commands!",
            color=discord.Color.blue()
        )
        return await message.channel.send(embed=embed)

    await bot.process_commands(message)

if __name__ == '__main__':
    keep_alive()
    print("-> Background Web Server Started!")
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        print("💥 BOT_TOKEN is missing! Please configure config.py or environment variables.")