import os
import json
import discord
from discord.ext import commands
import config
from core import ai, metrics, docker_client, smart

CHAT_CHANNEL_ID = int(os.environ["BRAMHA_CHAT_CHANNEL_ID"])
HISTORY_FILE = "/app/data/conversation_history.json"

conversations: dict[int, list[dict]] = {}

PERSONALITY = (
    "You're the AI living inside this homelab's Discord bot. You're witty, "
    "a little sarcastic, genuinely helpful — think sysadmin friend who's "
    "seen some things, not a corporate support bot. You can answer anything, "
    "server-related or totally unrelated (general knowledge, banter, etc). "
    "When asked about the server, ground your answer in the live data below "
    "rather than guessing. If something's actually broken (unhealthy "
    "container, bad SMART status), say so plainly first, joke after.\n\n"
)


def load_history():
    global conversations
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                raw = json.load(f)
                conversations = {int(k): v for k, v in raw.items()}
        except Exception:
            conversations = {}


def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(conversations, f)
    except Exception as e:
        print(f"Failed to save conversation history: {e}")


def gather_context() -> str:
    parts = [PERSONALITY]

    try:
        cpu = metrics.get_cpu()
        mem = metrics.get_memory()
        temps = metrics.get_temps()
        temp_line = f"{temps['avg']:.0f}°C avg, {temps['max']:.0f}°C max" if temps else "unavailable"
        parts.append(f"CPU: {cpu['percent']:.1f}%, Memory: {mem['percent']:.1f}%, Temperature: {temp_line}")
    except Exception as e:
        parts.append(f"Resource stats: error reading ({e})")

    try:
        docker_summary = docker_client.container_summary()
        container_list = docker_client.container_details_for_ai()
        parts.append(f"Docker: {docker_summary['running']}/{docker_summary['total']} running")
        parts.append(f"Containers:\n{container_list}")
    except Exception as e:
        parts.append(f"Docker info: error reading ({e})")

    try:
        disks = metrics.get_disks()
        disk_lines = [
            f"  - {d['label']}: {d['used_gb']:.1f}/{d['total_gb']:.1f} GB ({d['percent']:.1f}%)"
            for d in disks
        ]
        parts.append("Storage:\n" + "\n".join(disk_lines))
    except Exception as e:
        parts.append(f"Storage: error reading ({e})")

    try:
        smart_data = smart.get_all_smart()
        smart_lines = [
            f"  - {d['device']} ({d['label']}): {d['health']}" + (f", {d['temp_c']}°C" if d.get("temp_c") else "")
            for d in smart_data
        ]
        parts.append("Disk SMART health:\n" + "\n".join(smart_lines))
    except Exception as e:
        parts.append(f"SMART: error reading ({e})")

    try:
        entries = config.recent_audit(5)
        if entries:
            lines = [f"  - {e['ts']}: {e['username']} {e['action']} {e['target']} ({e['result']})" for e in entries]
            parts.append("Recent admin actions:\n" + "\n".join(lines))
    except Exception:
        pass

    return "\n\n".join(parts)


class AIBossCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        load_history()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != CHAT_CHANNEL_ID:
            return

        history = conversations.setdefault(message.channel.id, [])
        history.append({"role": "user", "content": message.content})

        async with message.channel.typing():
            try:
                context = gather_context()
                reply = await ai.chat(history, context)
            except Exception as e:
                reply = f"⚠️ Something went wrong talking to my backend: `{e}`"

        history.append({"role": "assistant", "content": reply})
        conversations[message.channel.id] = history[-40:]
        save_history()

        for chunk_start in range(0, len(reply), 1900):
            await message.channel.send(reply[chunk_start:chunk_start + 1900])


async def setup(bot: commands.Bot):
    await bot.add_cog(AIBossCog(bot))
