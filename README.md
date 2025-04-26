# Discord Game Server Status Bot 🎮

A customizable Discord bot that monitors and displays game server status using BattleMetrics API. Originally designed for Arma Reforger but adaptable to any game supported by BattleMetrics.

![Bot Example]  https://imgur.com/a/29zCVL6

## Features ✨
- Real-time server monitoring (Online/Offline status)
- Player count tracking
- Current map and version information
- Automatic updates every 5 minutes
- Slash command integration (`/GameStatus`)
- Customizable server list (supports up to 9 servers)

## Quick Start 🚀

### Prerequisites
- Python 3.8+
- Discord bot token
- BattleMetrics server IDs (optional)

### Installation
1. Install required packages:
   ```bash
   pip install discord.py requests

Save the file in the repo

TOKEN = "your_discord_bot_token"
GUILD_ID = 1234567890  # Your server ID
CHANNEL_ID = 1234567890  # Status channel ID

SERVERS = [
    {
        "name": "My Server",
        "ip": "1.2.3.4",
        "port": 2302,
        "bm_id": 12345678  # From BattleMetrics URL
    }
    # Add more servers...
]

**MAXIMUM OF 9 SERVERS**

title="🎮 YOUR_GAME_NAME Servers Status"
description="Current status of tracked Game server(s)"
color=0x00ff00  # Green color

Hosting Options ☁️
For Testing (Free)
Run locally with python bot.py

Use Replit + UptimeRobot for 24/7 uptime

For Production
DigitalOcean Droplet ($5/month)

AWS EC2 Free Tier

Raspberry Pi (for always-on home hosting)
