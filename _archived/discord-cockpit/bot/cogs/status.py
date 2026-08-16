import discord
from discord import app_commands
from discord.ext import commands

from core import metrics
from core.docker_client import container_summary


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="status", description="Show the homelab health dashboard")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()

        cpu = metrics.get_cpu()
        mem = metrics.get_memory()
        disks = metrics.get_disks()
        temps = metrics.get_temps()
        host = metrics.get_host_info()

        try:
            docker_summary = container_summary()
            docker_ok = True
        except Exception:
            docker_summary = None
            docker_ok = False

        embed = discord.Embed(
            title="🛰️  AJINKYA HOMELAB",
            description="**SYSTEM CONTROL CENTER**\n━━━━━━━━━━━━━━━━━━━━━━━━",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🧠 CPU",
            value=(
                f"`{metrics.bar(cpu['percent'])}` **{cpu['percent']:.1f}%**\n"
                f"load: {cpu['load'][0]:.2f}, {cpu['load'][1]:.2f}, {cpu['load'][2]:.2f} • {cpu['cores']} cores"
            ),
            inline=False
        )

        embed.add_field(
            name="💾 MEMORY",
            value=(
                f"`{metrics.bar(mem['percent'])}` **{mem['percent']:.1f}%**\n"
                f"{mem['used_gb']:.1f} / {mem['total_gb']:.1f} GB • swap {mem['swap_percent']:.0f}%"
            ),
            inline=False
        )

        for disk in disks:
            embed.add_field(
                name=f"🗄️ {disk['label']}",
                value=(
                    f"`{metrics.bar(disk['percent'])}` **{disk['percent']:.1f}%**\n"
                    f"{disk['used_gb']:.1f} / {disk['total_gb']:.1f} GB"
                ),
                inline=True
            )

        if temps:
            embed.add_field(
                name="🌡️ TEMP",
                value=f"avg **{temps['avg']:.0f}°C** • max **{temps['max']:.0f}°C**",
                inline=True
            )

        if docker_ok:
            d = docker_summary
            status_line = f"🟢 {d['running']} running"
            if d["stopped"]:
                status_line += f" • 🔴 {d['stopped']} stopped"
            if d["unhealthy"]:
                status_line += f" • ⚠️ {d['unhealthy']} unhealthy"
            embed.add_field(
                name="🐳 DOCKER",
                value=f"{status_line}\n{d['total']} containers total",
                inline=False
            )
        else:
            embed.add_field(
                name="🐳 DOCKER",
                value="⚠️ could not reach Docker socket",
                inline=False
            )

        embed.add_field(name="⏱️ UPTIME", value=f"`{host['uptime']}`", inline=True)
        embed.add_field(name="🌐 HOST", value=f"`{host['hostname']}`", inline=True)
        embed.add_field(name="🐧 OS", value=f"`{host['os']}`", inline=False)

        embed.set_footer(text="Ajinkya Homelab • Live telemetry")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="ping", description="Check whether the cockpit is responding")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🟢 **Cockpit Online** • `{latency} ms`")


async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))
