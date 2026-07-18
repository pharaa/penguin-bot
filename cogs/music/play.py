import discord
from discord.ext import commands
from collections import deque
import asyncio
import yt_dlp


async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)


class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.SONG_QUEUES = {}

    async def play_next_song(self, voice_client: discord.VoiceClient, guild_id, channel):
        if self.SONG_QUEUES[guild_id]:
            audio_url, title = self.SONG_QUEUES[guild_id].popleft()

            ffmpeg_options = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn -c:a libopus -b:a 96k",
            }

            source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin/ffmpeg")

            def after_play(error):
                if error:
                    print(f"Ошибка воспроизведения {title}: {error}")
                asyncio.run_coroutine_threadsafe(self.play_next_song(voice_client, guild_id, channel), self.bot.loop)

            voice_client.play(source, after=after_play)
            asyncio.create_task(channel.send(f"Сейчас играет: **{title}**"))
        else:
            await voice_client.disconnect()
            self.SONG_QUEUES[guild_id] = deque()

    @discord.app_commands.command(name="play", description="Подключиться, воспроизвести трек, добавить трек в очередь")
    @discord.app_commands.describe(song_query="Ссылка (YouTube/SoundCloud)")
    async def play(self, interaction: discord.Interaction, song_query: str):
        await interaction.response.defer()

        voice_channel = interaction.user.voice.channel

        if voice_channel is None:
            await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Ошибка",
                description="Вы обязаны быть в войсе"
            ))
            return

        voice_client = interaction.guild.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)

        ydl_options = {
            "format": "bestaudio[abr<=96]/bestaudio",
            "noplaylist": True,
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
        }

        if song_query.startswith(('http://', 'https://')):
            query = song_query
        else:
            query = f"ytsearch1: {song_query}"

        try:
            results = await search_ytdlp_async(query, ydl_options)
        except Exception as e:
            await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Ошибка",
                description=f"Не удалось получить трек: {e}"
            ))
            return

        if not results:
            await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Ошибка",
                description="Ничего не найдено"
            ))
            return

        if "entries" in results:
            if not results["entries"]:
                await interaction.followup.send(embed=discord.Embed(
                    color=0x000000,
                    title="Ошибка",
                    description="Ничего не найдено"
                ))
                return
            first_track = results["entries"][0]
        else:
            first_track = results

        audio_url = first_track.get("url")
        title = first_track.get("title", "Untitled")

        guild_id = str(interaction.guild_id)
        if self.SONG_QUEUES.get(guild_id) is None:
            self.SONG_QUEUES[guild_id] = deque()

        self.SONG_QUEUES[guild_id].append((audio_url, title))

        if voice_client.is_playing() or voice_client.is_paused():
            await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Готово",
                description=f"Добавлено в очередь:\n{title}"
            ))
        else:
            await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Продолжаем",
                description=f"Сейчас играет:\n{title}"
            ))
            await self.play_next_song(voice_client, guild_id, interaction.channel)

    @discord.app_commands.command(name="stop", description="Остановить всё")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.defer()
        voice_client = interaction.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send(embed=discord.Embed(
                color=0x000000,
                title="Ошибка",
                description="Бот не в канале"
            ))

        await interaction.followup.send(embed=discord.Embed(
            color=0x000000,
            title="Готово",
            description="Остановлено"
        ))

        guild_id_str = str(interaction.guild_id)
        if guild_id_str in self.SONG_QUEUES:
            self.SONG_QUEUES[guild_id_str].clear()

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
