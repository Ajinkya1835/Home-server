import discord
from discord import app_commands
from discord.ext import commands

from core import metrics, smart


def health_emoji(health: str) -> str:
    if health == "PASSED":
        return "🟢"
    if health == "ERROR" or health == "UNKNOWN":
        return "⚠️"
    return "🔴"


class DiskCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="disk", description="Storage and SMART health dashboard")
    async def disk(self, interaction: discord.Interaction):
        await interaction.response.defer()

        disks = metrics.get_disks()
        smart_data = smart.get_all_smart()

        embed = discord.Embed(
            title="🗄️ STORAGE & DISK HEALTH",
            color=discord.Color.orange(),
        )

        for disk in disks:
            embed.add_field(
                name=disk["label"],
                value=(
                    f"`{metrics.bar(disk['percent'])}` **{disk['percent']:.1f}%**\n"
                    f"{disk['used_gb']:.1f} / {disk['total_gb']:.1f} GB"
                ),
                inline=True,
            )

        for d in smart_data:
            icon = health_emoji(d["health"])
            if d["health"] == "ERROR":
                value = f"{icon} Could not read SMART data\n`{d.get('error', 'unknown error')}`"
            else:
                lines = [f"{icon} **{d['health']}**"]
                if d.get("temp_c"):
                    lines.append(f"Temp: {d['temp_c']}°C")
                if d.get("reallocated_sectors") is not None:
                    lines.append(f"Reallocated sectors: {d['reallocated_sectors']}")
                if d.get("pending_sectors") is not None:
                    lines.append(f"Pending sectors: {d['pending_sectors']}")
                if d.get("uncorrectable_sectors") is not None:
                    lines.append(f"Uncorrectable: {d['uncorrectable_sectors']}")
                value = "\n".join(lines)

            embed.add_field(
                name=f"S.M.A.R.T — {d['label']} (`{d['device']}`)",
                value=value,
                inline=False,
            )

        embed.set_footer(text="Ajinkya Homelab • Disk & SMART telemetry")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DiskCog(bot))
