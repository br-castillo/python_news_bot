import discord
from discord.ext import commands, tasks
import datetime
from ruamel.yaml import YAML
import os
import requests
import logging
import random
from itertools import cycle
import asyncio
import re
import json
import time
import newsbotapi as newsbot

yaml = YAML()

with open("./config.yml", "r", encoding = "utf-8") as file:
    config = yaml.load(file)    

client = discord.Client()

'''
Bot Properties being read from Config.yml
'''

# Channel ID's
log_channel_id = config["Log Channel ID"]
main_channel_id = config["Main Channel ID"]

# Embedded Message Colors
client.embed_green = discord.Color.from_rgb(37, 225, 45)
client.embed_red = discord.Color.from_rgb(255, 0, 0)
client.embed_white = discord.Color.from_rgb(255, 250, 250)
client.embed_black = discord.Color.from_rgb( 0, 0, 0)
client.embed_lightblue = discord.Color.from_rgb(0, 175, 225)

# Embedded Message Properties
client.footer_text = config["Embed Settings"]["Footer"]["Text"]
client.newspaper_icon = config["Embed Settings"]["Footer"]["Icon URL"]

# Playing Status and Command Prefix setup
client.prefix = config["Prefix"]
client.playing_status = config["Playing Status"].format(prefix = client.prefix)

client.TOKEN = os.getenv(config["Bot Token Variable Name"])
token = client.TOKEN


'''
Bot event on start-up
'''

@client.event
async def on_ready():
    print(f"I am logged in as {client.user} and connected to Discord! ID: {client.user.id}")

    game = discord.Game(name = "Checking News")
    await client.change_presence(activity = game)
    
    embed = discord.Embed(
        title = f"{client.user.name} Online!" ,
        description = "Remember to always take news with a grain of salt, do your own due dilligence, and not trade solely based off of news!", 
        color = client.embed_green ,
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        )

    embed.set_footer(
        text = client.footer_text,
        icon_url = client.newspaper_icon)

    print('-----')
    client.log_channel = client.get_channel(log_channel_id)
    await client.log_channel.send(embed = embed)

    checker = True
    sent_articles = []

    async def news_checker():
        newsbot.news_grabber()
        
        with open("data.json") as json_file:
            data = json.load(json_file)
            news = data['articles']
            news_articles = []
            for x, y in enumerate(news):
                news_articles.append([x, [y['title'], y['url'], y['urlToImage'], y['source']['name']]])
        
        counter = 0
        print('Now starting news checker.')
        
        for counter in range(0,10):
            embed = discord.Embed(
            title = news_articles[counter][1][0],
            url = news_articles[counter][1][1],
            description = news_articles[counter][1][3],
            color = client.embed_white,
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            )

            if news_articles[counter][1][2] is None: 
                embed.set_image(
                url = ('https://cdn2.iconfinder.com/data/icons/picol-vector/32/news-512.png'))
            else:
                embed.set_image(
                url = news_articles[counter][1][2])
            
            embed.set_footer(
            text = client.footer_text,
            icon_url = client.newspaper_icon)

            if news_articles[counter][1][1] not in sent_articles:
                client.log_channel = client.get_channel(log_channel_id)
                await asyncio.sleep(2)
                await client.log_channel.send(embed=embed)
                print("Article titled '{}' was successfully sent.".format(news_articles[counter][1][0]))
                sent_articles.append(news_articles[counter][1][1])
                counter += 1
            elif news_articles[counter][1][1] in sent_articles:
                await asyncio.sleep(2)
                print("Article titled '{}' already sent, skipping article.".format(news_articles[counter][1][0]))
                counter += 1
                continue
            elif counter == 10:
                break

        if counter == 10:
            print('Loop finished.')
            print('-----')
            counter = 0

    while checker == True and request != 100:
        request += 1
        await news_checker()
        print("-----")
        print(f"Request number {request}")
        await asyncio.sleep(300)
         
        if request == 100:
          print("-----")
          print("Maximum number of requests sent today, now shutting off.")
          break

client.run('NzYzNzk0NzQ5Nzg5NTY5MDk0.X385Sg.XEiveRjmAgpRYDQHamTTWhbnOG4')