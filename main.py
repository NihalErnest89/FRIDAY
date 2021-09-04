#Coded by Nihal Ernest (IronManForever)
#4 September 2021
#For the Helloo Hacks II
#In order to run the program, run main.exe in dist folder

import datetime

import discord
from discord import client
from discord.ext import commands

import requests
import json
import time

from discord.utils import get

bot = commands.Bot(command_prefix='!')

@bot.command(help='tells a joke')
async def joke(ctx):
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    j = response.json()
    await ctx.send(j["setup"])
    time.sleep(5)
    await ctx.send(j["punchline"])

@bot.command(help='clears certain number of messages')
async def clear(ctx, num=6):
    if 0 < num <= 50:
        await ctx.channel.purge(limit=num + 1)
    else:
        await ctx.send('Please enter a valid number (1-50)')

@bot.command(help='kicks someone from the server')
async def kick(ctx, member:discord.Member, reason='You have been kicked!'):
    await member.kick(reason=reason)

@bot.command(help='moves all connected users to specifiec voice channel')
async def moveall(ctx, channel : discord.VoiceChannel):
    #await ctx.send(ctx.author.voice.channel.members)
    for i in ctx.author.voice.channel.members:
        await i.move_to(channel)

@bot.command(help='moves a connected user to another voice channel')
async def move(ctx, member : discord.Member, channel : discord.VoiceChannel):
    await member.move_to(channel)

@bot.command(help='annoys the person')
async def annoy(ctx, name, height=5):
    if height > 9:
        await ctx.send('Invalid input, try again')
        return
    content = name
    out = ''
    for i in range(0, int(height)):
        out += content + '\n'
        content += ' ' + name
    for j in range(int(height), 0, -1):
        blank = ''
        for k in range(0, j - 1):
            blank += name + ' '
        out += blank + '\n'

    await ctx.send(out)

@bot.command(help='Returns weather based on city name')
async def weather(ctx, city):
    w_key = "Enter your API key here"
    url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + w_key + "&q=" + city
    response = requests.get(url)
    j = response.json()
    wind = j["wind"]["speed"]
    if j["cod"] != "404":
        m = j["main"]
        sunrise_time = datetime.datetime.fromtimestamp(j["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(j["sys"]["sunset"])
        temp = m["temp"] - 273.15
        f_temp = temp * (9 / 5) + 32
        embed = discord.Embed(title=city.title(), description="Weather Report",
                              colour=discord.Colour.blue())
        embed.add_field(name="Temperature", value=str(int(temp + 0.5)) + ' °C (' + str(int(f_temp + 0.5)) + '°F)', inline=False)
        embed.add_field(name="Humidity", value=str(m["humidity"]) + '%', inline=False)
        embed.add_field(name="Pressure", value=str(m["pressure"]) + ' hPa', inline=False)
        embed.add_field(name="Wind Speed", value=str(round((wind * 3.6), 1)) + ' km/h (' + str(round((wind * 2.236936), 1)) + 'mph)', inline=False)
        embed.add_field(name="Wind Direction", value=str(j["wind"]["deg"]) + ' degrees', inline=False)
        embed.add_field(name="Description", value=str(j["weather"][0]["description"]).title(), inline=False)
        embed.add_field(name="Sunrise", value=str(sunrise_time)[11:], inline=False)
        embed.add_field(name="Sunset", value=str(sunset_time)[11:], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Invalid input, try again')
@bot.event
async def on_ready():
    print('Project', bot.user.name, 'Online')

bot.run('Enter your API key here')