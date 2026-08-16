import discord
from discord import app_commands
from discord.ext import commands

import config
from core import docker_client, metrics


STATUS_ICON = {
    "running": "🟢",
    "exited": "🔴",
    "paused": "⏸️",
    "restarting": "🟡",
    "created": "⚪",
}


def status_icon(container) -> str:
    if container["health"] == "unhealthy":
        return "⚠️"
    return STATUS_ICON.get(container["status"], "⚪")


class ContainerSelect(discord.ui.Select):
    def __init__(self, containers):
        options = [
            discord.SelectOption(
                label=c["name"],
                description=f"{c['status']}" + (f" ({c['health']})" if c["health"] else ""),
                emoji=status_icon(c),
            )
            for c in containers[:25]
        ]
        super().__init__(placeholder="Select a container...", options=options)

    async def callback(self, interaction: discord.Interaction):
        name = self.values[0]
        view = ContainerActionView(name)
        embed = build_container_embed(name)
        await interaction.response.edit_message(embed=embed, view=view)


class ContainerDashboardView(discord.ui.View):
    def __init__(self, containers):
        super().__init__(timeout=120)
        self.add_item(ContainerSelect(containers))


def build_container_embed(name: str) -> discord.Embed:
    container = docker_client.get_container(name)
    container.reload()

    embed = discord.Embed(
        title=f"🐳 {name}",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Status", value=container.status, inline=True)

    health = container.attrs.get("State", {}).get("Health", {}).get("Status")
    if health:
        embed.add_field(name="Health", value=health, inline=True)

    image = container.image.tags[0] if container.image.tags else container.image.short_id
    embed.add_field(name="Image", value=f"`{image}`", inline=False)

    if container.status == "running":
        try:
            stats = docker_client.container_stats(name)
            embed.add_field(
                name="CPU",
                value=f"`{metrics.bar(stats['cpu_percent'])}` {stats['cpu_percent']:.1f}%",
                inline=False,
            )
            embed.add_field(
                name="Memory",
                value=(
                    f"`{metrics.bar(stats['mem_percent'])}` {stats['mem_percent']:.1f}%\n"
                    f"{stats['mem_usage_mb']:.0f} / {stats['mem_limit_mb']:.0f} MB"
                ),
                inline=False,
            )
        except Exception:
            embed.add_field(name="Stats", value="unavailable", inline=False)

    return embed


class ContainerActionView(discord.ui.View):
    def __init__(self, name: str):
        super().__init__(timeout=120)
        self.name = name

    @discord.ui.button(label="Logs", style=discord.ButtonStyle.secondary, emoji="📜")
    async def logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        logs = docker_client.container_logs(self.name, tail=30)
        if len(logs) > 1900:
            logs = logs[-1900:]
        await interaction.followup.send(f"```\n{logs or '(no logs)'}\n```", ephemeral=True)

    @discord.ui.button(label="Stats", style=discord.ButtonStyle.secondary, emoji="📊")
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=build_container_embed(self.name), view=self)

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary, emoji="🔄")
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not config.is_admin(interaction.user.id):
            await interaction.response.send_message("🚫 Admin only.", ephemeral=True)
            return
        await interaction.response.send_message(
            f"⚠️ Restart **{self.name}**?",
            view=ConfirmView(self.name, "restart"),
            ephemeral=True,
        )

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not config.is_admin(interaction.user.id):
            await interaction.response.send_message("🚫 Admin only.", ephemeral=True)
            return
        if self.name in config.PROTECTED_CONTAINERS:
            await interaction.response.send_message(
                f"🚫 **{self.name}** is protected and can't be stopped from here.", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"⚠️ Stop **{self.name}**? This will take the service offline.",
            view=ConfirmView(self.name, "stop"),
            ephemeral=True,
        )


class ConfirmView(discord.ui.View):
    def __init__(self, name: str, action: str):
        super().__init__(timeout=15)
        self.name = name
        self.action = action

    @discord.ui.button(label="Yes, confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if self.action == "restart":
                docker_client.restart_container(self.name)
            elif self.action == "stop":
                docker_client.stop_container(self.name)
            await interaction.response.edit_message(
                content=f"✅ {self.action}ed **{self.name}**.", view=None
            )
        except Exception as e:
            await interaction.response.edit_message(
                content=f"❌ Failed to {self.action} **{self.name}**: `{e}`", view=None
            )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Cancelled.", view=None)


class DockerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="docker", description="Docker container dashboard")
    async def docker_dashboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        containers = docker_client.list_containers()
        if not containers:
            await interaction.followup.send("No containers found.")
            return

        embed = discord.Embed(
            title="🐳 Docker Dashboard",
            description=f"{len(containers)} containers • select one below",
            color=discord.Color.blurple(),
        )
        view = ContainerDashboardView(containers)
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(DockerCog(bot))
