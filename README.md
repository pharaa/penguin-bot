# Penguin Bot

A simple, lightweight Discord bot designed for music playback, chat archiving, antispam tools, and channel management. Built using `discord.py` and `yt-dlp`.

## Features
- **High-Quality Music:** Play and stream audio tracks directly from **YouTube** and **SoundCloud**.
- **Queue System:** Automatically manage music queues with seamless integration for pausing, skipping, resuming, and stopping tracks.
- **Server Moderation:** Basic antispam controls and specialized channel auto-moderation tools.

## Prerequisites
Before you begin, make sure you have installed:
- **Python 3.10+**
- **FFmpeg:** Installed on your system and added to your environment's PATH variable (or reference the local path in `play.py`).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pharaa/penguin-bot.git
   cd penguin-bot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install Required Packages:**
   Install `discord.py` with voice dependencies along with audio streaming and encryption packages:
   ```bash
   pip install -U "discord.py[voice]" yt-dlp python-dotenv pynacl davey
   ```

4. **Add Your Bot Token:**
   Create a file named `token.txt` in the root directory of the project and insert your Discord Bot Token inside it:
   ```text
   YOUR_DISCORD_BOT_TOKEN_GOES_HERE
   ```

5. **Configure Server Settings:**
   Open `main.py` and replace the placeholder variables with your actual Discord server and targeted channel IDs:
   ```python
   CHANNEL_ID = 1518733975320006808
   GUILD_ID = 1518017112738627696
   ```

## Running the Bot
Once everything is configured, start your bot by running:
```bash
python main.py
```
