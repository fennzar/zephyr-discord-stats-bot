# Zephyr Discord Stats Bot

The Zephyr Discord Stats Bot is a dedicated Discord bot designed to track and display various statistics for the Zephyr Protocol within a Discord server. This bot is ideal for crypto communities who wish to keep their members updated on the latest stats without leaving Discord. While it's tailored for the Zephyr Protocol, it could be adaptated for other cryptocurrency communities.

It simply updates voice channel names to display the latest stats.

## Getting Started

### Prerequisites

- Python 3.8 or higher.
- `discord.py` library.
- `requests` library for API calls.

### Installation

1. Clone the repository:
2. Update apis.py with your own API calls
3. Optionally update and use daemon.py to define rpc calls to the daemon
4. Redefine and update channel ids in bot.py

### Run

`python3 bot.py`

#

### How to create an invite a bot

Create a bot on the Discord Developer Portal.
https://discord.com/developers/applications

1. Create a new application
2. Go to the “Bot” section and click on “Add Bot”.
3. Get bot token from "Bot" section
4. Go to the “OAuth2” section and select “bot” in the “Scopes” section.
5. Make sure you select "Manage Channels" to allow the bot to update channel names.
6. Copy the link and paste it into your browser. Select the server you want to add the bot to and click “Authorize”.
