import discord
from discord.ext import tasks
from discord import app_commands
import requests
import asyncio


# THIS IS SIMPLY A PYTHON SCRIPT TO RUN YOUR BOT WITH, THIS IS ASSUMING YOU HAVE A BOT MADE HERE @ : https://discord.com/developers/applications
# YOU WILL NEED DISCORD.PY

# Replace these with your actual credentials
TOKEN = "YOUR_ACTUAL_TOKEN"
GUILD_ID = YOUR SERVER ID  # Your server ID
CHANNEL_ID = YOUR CHANNEL ID  # Channel ID for auto-updates

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 

# recommend max 9 servers due to discord embed size
 #bm_id pulled from battlemetrics.com
SERVERS = [ 
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789}, # if using bm_id, last digits at the end of URL are your bm_id
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789},
    {"name": "INSERT_SERVER_NAME", "ip": "IP_HERE", "port": PORT_HERE, "bm_id": 123456789}
]

def get_server_data(bm_id):
    if not bm_id:
        return {"status": "UNKNOWN", "players": "?", "max_players": "?", "map": "?", "version": "?"}
    
    try:
        url = f"https://api.battlemetrics.com/servers/{bm_id}"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        
        attr = data["data"]["attributes"]
        det = attr.get("details", {})
        
        return {
            "status": attr.get("status", "unknown").upper(),
            "players": attr.get("players", "?"),
            "max_players": attr.get("maxPlayers", "?"),
            "map": det.get("map", "Unknown"),
            "version": det.get("version", "Unknown"),
        }
    except requests.exceptions.RequestException:
        return {"status": "API ERROR", "players": "?", "max_players": "?", "map": "?", "version": "?"}
    except (KeyError, ValueError):
        return {"status": "DATA ERROR", "players": "?", "max_players": "?", "map": "?", "version": "?"}

def build_embed():
    embed = discord.Embed(
        title="🎮 Arma Reforger Servers Status",
        color=0x00ff00,
        description="Current status of tracked Arma Reforger servers"
    )
    
    for server in SERVERS:
        info = get_server_data(server["bm_id"])
        
        # Debug print
        print(f"Processing: {server['name']} - Status: {info['status']}")
        
        # Skip if we hit field limits
        if len(embed.fields) >= 24:
            embed.add_field(name="⚠️ Note", value="Some servers not shown due to Discord limits", inline=False)
            break
            
        # Add field
        embed.add_field(
            name=f"{server['name']} ({info['status']})",
            value=(
                f"🧑 Players: {info['players']}/{info['max_players']}\n"
                f"🗺️ Map: {info['map']}\n"
                f"🧩 Version: {info['version']}\n"
                f"🔌 {server['ip']}:{server['port']}"
            ),
            inline=False
        )
    
    embed.set_footer(text="Updated every 5 minutes | Data from BattleMetrics")
    return embed

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    status_loop.start()

@tree.command(name="armaservers", description="Show current status of Arma Reforger servers", guild=discord.Object(id=GUILD_ID))
async def armaservers(interaction: discord.Interaction):
    embed = build_embed()
    await interaction.response.send_message(embed=embed)

@tasks.loop(minutes=5)
async def status_loop():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            embed = build_embed()
            # Find and edit previous message if it exists
            async for message in channel.history(limit=1):
                if message.author == client.user:
                    await message.edit(embed=embed)
                    return
            # If no previous message found, send new one
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Error updating status: {e}")

client.run(TOKEN)