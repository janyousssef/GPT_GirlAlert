import discord
from discord import Intents
from discord.ext import commands
import asyncio
import aiohttp
from pydub import AudioSegment
from io import BytesIO
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

#bot = commands.Bot(command_prefix='!')

async def play_sound(voice_client, file_path, duration):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(2).set_frame_rate(48000)
    byte_data = BytesIO()
    audio.export(byte_data, format="s16le")
    byte_data.seek(0)
    print("line 21")
    voice_client.stop()
    voice_client.play(discord.PCMVolumeTransformer(
        discord.PCMAudio(byte_data)))
    await asyncio.sleep(duration)
    voice_client.stop()
    await voice_client.disconnect()

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel and after.channel is not None:
        girl_role = discord.utils.get(member.guild.roles, name="girls")
        if girl_role in member.roles:
            voice_channel = after.channel
            if voice_channel is not None:
                if voice_channel.guild.voice_client is None:
                    voice_client = await voice_channel.connect()
                else:
                    voice_client = voice_channel.guild.voice_client
                print("playing sound")
                await play_sound(voice_client, "audio.mp3", 3)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    dir_list = os.listdir(".")
    print("Files and directories in '", ".", "' :")
    print(dir_list)
    
my_secret = os.environ['TOKEN']
bot.run(my_secret)
