import discord
import asyncio
import random
import os
import re
import ast
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
# import psutil
import traceback
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')
TOKEN = os.environ['TOKEN']
client = discord.Client()



@client.event
async def on_message(message):


    if message.content=='^^ping':
        await message.channel.send(embed=discord.Embed(
            title=f'Pong!',
            description=f"`{round(client.latency)*1000, 2}ms`")
        )
    



client.run(TOKEN)
