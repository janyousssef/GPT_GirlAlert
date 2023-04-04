import discord
from discord.ext import commands
import asyncio
import aiohttp
from pydub import AudioSegment
from io import BytesIO

bot = commands.Bot(command_prefix='!')


async def preload_audio(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            audio = AudioSegment.from_file(BytesIO(data), format="mp3")
            audio = audio.set_channels(2).set_frame_rate(48000)
            byte_data = BytesIO()
            audio.export(byte_data, format="s16le")
            byte_data.seek(0)
    return byte_data


async def play_sound(voice_client, url, duration):
    byte_data = await preload_audio(url)
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
                #await play_sound(voice_client, "https://sndup.net/nttr/d", 5.8) # اختاااااه احذري
                #await play_sound(voice_client, "https://sndup.net/gbkd/d", 3) #انت بتتكلمي كدا ليه يا مرا
                await play_sound(voice_client, "https://www.myinstants.com/media/sounds/damaged_coda.mp3", 25) # اسكت


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run("MTA5MDA3Njk2MTY5MjQ1OTA0OQ.Gb3G0b.rTpiDjzbpeM6mLCY5x-LK2-uls8twfEQv37wMY")
