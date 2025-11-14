# 🧹 Discord Cleanup Bot

A safe, UI-protected cleanup bot designed to delete:

✅ Custom Roles

✅ Server Emojis

✅ Server Stickers

Nothing else is touched.

This bot uses a two-step interactive confirmation system to prevent accidental or unauthorized use — making it suitable for server resets, testing environments, or controlled server cleanup.

⚠️ The bot does NOT delete channels, users, or messages.
It is not a nuker — only a cleanup utility.

✨ Features
Feature	Status
Deletes roles (except @everyone and system roles)	✔️
Deletes custom emojis	✔️
Deletes server stickers	✔️
Double confirmation button system	✔️
Logs everything to a cleanup_log.json file	✔️
Only the command initiator can confirm actions	✔️
🚀 Setup (GitHub Codespace Recommended)
1. Fork or Clone the Repo
git clone https://github.com/cosmonium0/cord-cleaner
cd discord-cleanup-bot

2. Install Requirements
pip install -r requirements.txt

3. Add Bot Token (Secure)
Option A — Codespaces Secret (Recommended)

Go to: Repo → Settings → Codespaces → Secrets

Create secret named:

DISCORD_TOKEN


Paste your bot token from the Discord Developer Portal.

Option B — .env File (Local Only)
DISCORD_TOKEN=YOUR_TOKEN_HERE


Make sure .env is in .gitignore so it never uploads.

4. Enable Bot Permissions

In the Discord Developer Portal → Bot settings, enable:

✔️ MESSAGE CONTENT INTENT

✔️ SERVER MEMBERS INTENT

✔️ Presence Intent (optional)

✔️ Permissions:

Manage Roles

Manage Emojis and Stickers

Invite the bot using the proper OAuth2 link with these scopes:

bot applications.commands

5. Run the Bot
python bot.py


If the setup is correct, you’ll see:

Logged in as CleanupBot#0000

📌 Usage

In any server channel where the bot has access:

!cleanup


The bot will:

Send a warning message with Proceed / Cancel buttons.

Require a second confirmation with a DELETE EVERYTHING button.

Nothing executes until the user presses both confirmations.

Only the person who started the process can confirm.

📁 Logs

After cleanup, a file like:

cleanup_log_1234567890123.json


will be generated, containing:

Deleted role names & IDs

Deleted emoji names & IDs

Deleted sticker names & IDs

Timestamp

Who executed the cleanup

🛡️ Safety Notes

The bot cannot be used silently — all actions require interactive confirmation.

Users without button access cannot trigger the cleanup even if they type the command.

This bot is intended for legitimate server administration only.

📌 Roadmap (Optional Future Add-Ons)

☐ Backup emojis & stickers before deletion

☐ Web dashboard delete button

☐ Slash command version

☐ “Undo mode” (rebuild deleted roles only)

☐ Run only once per 24 hours cooldown
