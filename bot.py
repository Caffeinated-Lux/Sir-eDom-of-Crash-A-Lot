import discord
from discord.ext import commands
import responses
import os
from dotenv import load_dotenv

# Load the variables from the .env file
load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')

    # 1. Setup Intents
    intents = discord.Intents.default()
    intents.message_content = True

    # 2. Initialize Bot - command_prefix handles the "!" automatically
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} is operational. DMs are disabled.")
        for guild in bot.guilds:
            print(f" -> Active in: {guild.name}")

    # 3. Create a command for everything
    @bot.command(name="country")
    async def country(ctx, cid: str = "17"):
        async with ctx.typing():
            # We specifically pass the command to the handler
            response = responses.handle_response(f"country {cid}")
            await ctx.send(response)

    @bot.command(name="rws")
    async def rws(ctx):
        async with ctx.typing():
            response = responses.handle_response("rws")
            await ctx.send(response)

    @bot.command(name="help")
    async def help_command(ctx):
        response = responses.handle_response("help")
        await ctx.send(response)

    # 4. Error Handler - Prevents the bot from trying to send DMs on errors
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        print(f"⚠️ Error: {error}")

    bot.run(TOKEN)
