import os

import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INITIAL_COGS = [
    "cogs.status",
    "cogs.docker_ctl",
    "cogs.disk",
    "cogs.ai_boss",
]
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    print(f"COMMAND ERROR: {error!r}")
    import traceback
    traceback.print_exception(type(error), error, error.__traceback__)
    try:
        if interaction.response.is_done():
            await interaction.followup.send(f"❌ Error: `{error}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Error: `{error}`", ephemeral=True)
    except Exception:
        pass
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="the homelab 🖥️"
        )
    )

    synced = await bot.tree.sync()

    print("=" * 50)
    print(f"ONLINE: {bot.user}")
    print(f"Slash commands: {len(synced)}")
    print("=" * 50)


async def main():
    async with bot:
        for cog in INITIAL_COGS:
            await bot.load_extension(cog)
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
