import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime, timezone
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def now():
    return datetime.now(timezone.utc).isoformat()


class SecondConfirmView(discord.ui.View):
    def __init__(self, ctx, log):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.log = log

    @discord.ui.button(label="DELETE EVERYTHING", style=discord.ButtonStyle.danger)
    async def delete_all(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("❌ You did not start this action.", ephemeral=True)

        await interaction.response.send_message("🧹 Cleaning roles, emojis, and stickers...")

        guild = self.ctx.guild

        # --- Delete Roles ---
        for role in guild.roles[::-1]:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete(reason="Cleanup Bot Operation")
                self.log["roles"].append({"name": role.name, "id": role.id})
                await asyncio.sleep(0.5)
            except:
                pass

        # --- Delete Emojis ---
        for emoji in guild.emojis:
            try:
                await emoji.delete(reason="Cleanup Bot Operation")
                self.log["emojis"].append({"name": emoji.name, "id": emoji.id})
                await asyncio.sleep(1)
            except:
                pass

        # --- Delete Stickers ---
        for sticker in guild.stickers:
            try:
                await sticker.delete(reason="Cleanup Bot Operation")
                self.log["stickers"].append({"name": sticker.name, "id": sticker.id})
                await asyncio.sleep(1)
            except:
                pass

        # SAVE LOG
        filename = f"cleanup_log_{guild.id}_{int(datetime.now().timestamp())}.json"
        with open(filename, "w") as f:
            json.dump(self.log, f, indent=2)

        await interaction.followup.send(
            f"✅ Cleanup complete.\n🗂 Log stored as `{filename}`."
        )
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("❌ You cannot cancel this.", ephemeral=True)

        await interaction.response.send_message("🛑 Cleanup canceled.")
        self.stop()



class FirstConfirmView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @discord.ui.button(label="Proceed", style=discord.ButtonStyle.danger)
    async def proceed(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("❌ You are not the command initiator.", ephemeral=True)

        log = {
            "guild": interaction.guild.name,
            "guild_id": interaction.guild.id,
            "executed_by": interaction.user.id,
            "timestamp": now(),
            "roles": [],
            "emojis": [],
            "stickers": []
        }

        await interaction.response.send_message(
            "⚠️ **FINAL WARNING:** This will delete **ALL roles, emojis, and stickers.**\n"
            "This action cannot be undone.\n\n"
            "Click CONFIRM to execute.",
            view=SecondConfirmView(self.ctx, log)
        )
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("❌ Not your operation.", ephemeral=True)

        await interaction.response.send_message("🛑 Cleanup canceled.")
        self.stop()



@bot.command()
@commands.guild_only()
async def cleanup(ctx):
    """Starts the double-confirm cleanup UI."""
    await ctx.send(
        "🧹 **Cleanup Initiated**\n"
        "This will delete:\n"
        "• All Roles (except @everyone & bot-integrated roles)\n"
        "• All Custom Emojis\n"
        "• All Stickers\n\n"
        "Are you sure?",
        view=FirstConfirmView(ctx)
    )


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
      
