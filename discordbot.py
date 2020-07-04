import discord
import asyncio
import random
import os
import re
import ast
import gspread
import json
import sqlite3
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
            description=f"`{round((client.latency)*1000, 2)}ms`"))

    if message.content=='^^ping2':
        await message.channel.send(embed=discord.Embed(
            title=f'Pong!',
            description=f"`{(client.latency)*1000, 2)}ms`")
        
    if message.content == "^^makedb ":
        name = message.content.split(" ")[1]
        await message.channel.send(f"{name}")

        # データベースに接続する
        conn = sqlite3.connect(f'{name}.db')
        c = conn.cursor()

        # テーブルの作成
        c.execute('''CREATE TABLE users(id real, name text, birtyday text)''')

        # データの挿入
        c.execute("INSERT INTO users VALUES (1, '煌木 太郎', '2001-01-01')")
        c.execute("INSERT INTO users VALUES (2, '学習 次郎', '2006-05-05')")
        c.execute("INSERT INTO users VALUES (3, '牌存 花子', '2017-09-10')")

        # 挿入した結果を保存（コミット）する
        conn.commit()

        # データベースへのアクセスが終わったら close する
        conn.close()

    if message.content == "^^connectdb ":
        name = message.content.split(" ")[1]
        await message.channel.send(f"{name}")

        # データベースに接続する
        conn = sqlite3.connect(f'{name}.db')
        c = conn.cursor()

        # レコードを生年月日の降順で取得する
        for row in c.execute('SELECT * FROM users ORDER BY birtyday DESC'):
            await message.channel.send(f"{row}")

        # データベースへのアクセスが終わったら close する
        conn.close()
 
@client.event
async def on_raw_reaction_add(payload):
    
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
    m = await channel.send(f'`{role.name}`を{member.mention}に付与！')
    await asyncio.sleep(5)
    await m.delete()



client.run(TOKEN)
