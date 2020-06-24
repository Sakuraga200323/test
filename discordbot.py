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


ID_CHANNEL_README = 725486353151819899 # 該当のチャンネルのID
ID_ROLE_WELCOME = 719176372773453835 # 付けたい役職のID


@client.event
async def on_message(message):


    if message.content=='^^ping':
        await message.channel.send(embed=discord.Embed(
            title=f'Pong!',
            description=f"`{round((client.latency)*1000, 2)}ms`")
        )
    
    # channel_id から Channel オブジェクトを取得
    channel = client.get_channel(payload.channel_id)

    # 該当のチャンネル以外はスルー
    if channel.id != ID_CHANNEL_README:
        return

    # guild_id から Guild オブジェクトを取得
    guild = client.get_guild(payload.guild_id)

    # user_id から Member オブジェクトを取得
    member = guild.get_member(payload.user_id)

    # 用意した役職IDから Role オブジェクトを取得
    role = guild.get_role(ID_ROLE_WELCOME)

    # リアクションを付けたメンバーに役職を付与
    await member.add_roles(role)

    # 分かりやすいように歓迎のメッセージを送る
    m = await channel.send(f'{role.mention}を{member.mention}に付与！')
    await asyncio.sleep(5)
    await m.delete()



client.run(TOKEN)
