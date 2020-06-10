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


#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('player-data-279309-2da8d7ecf786.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1vdLj6XESe5f1sgUevYGtB7wpU5MyVzoomk5v4GtAzZc'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"^^help|機能停止中|{len(client.guilds)}の鯖が導入|"))
    NOW = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")
    # MEM = psutil.virtual_memory().percent
    LOG_CHANNELS = [i for i in client.get_all_channels() if i.name == "bit起動ログ"]
    desc = (f"\n+Bot\n{client.user}"
        + f"\n+BotID\n{client.user.id}"
        + f"\n+Prefix\n^^"
        # + f"\n+UseingMemory\n{MEM}%"
    )
    for ch in LOG_CHANNELS:
        try:
            embed = discord.Embed(
                title = "BitRPG起動ログ",
                description = f"```diff\n{desc}```")
            embed.timestamp = datetime.now(JST)
        except:
            print("Error")
    print(desc)

    path = f"data/playerdata/log/startup/{NOW}txt"
    with open(path,mode="w") as f:
        f.write(f"startup\n{datetime.now(JST)}")

@client.event
async def on_message(message):

    m_ctt = message.content
    m_em = message.embeds
    m_id = message.id
    m_ch = message.channel
    m_guild = message.guild
    m_author = message.author

    
    if m_ct.startswith("^^"):
        await m_ch.send("現在停止中です。")
    
    if m_ctt.startswith("^^test "):
        cell = m_ctt.split("test ")[1]
        #A1セルの値を受け取る
        import_value = int(worksheet.acell(cell).value)
        await m_ch.send(import_value)

client.run(TOKEN)
