import discord
import asyncio
import random
import os
import re
import ast
import gspread
import json
import redis
from oauth2client.service_account import ServiceAccountCredentials 
from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
from flask_sqlalchemy import SQLAlchemy
import traceback
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')
TOKEN = os.environ['TOKEN']
client = discord.Client()


ID_CHANNEL_README = 725486353151819899 # 該当のチャンネルのID
ID_ROLE_WELCOME = 719176372773453835 # 付けたい役職のID

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)

db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Entry(db.Model):
    # テーブル名を定義
    __tablename__ = "entries"

    # カラムを定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

    
    
@client.event
async def on_message(message):

    if message.content=='^^ping':
        await message.channel.send(embed=discord.Embed(
            title=f'Pong!',
            description=f"`{round((client.latency)*1000, 2)}ms`"))

    if message.content == '^^ping2':
        await message.channel.send(
            embed=discord.Embed(
                title=f'Pong!',
                description=f"`{(client.latency)*1000, 2}ms`"
            )
        )

    if message.content.startswith("^^adddb "):
        key = message.content.split(" ")[1]
        value = message.content.split(" ")[2]
        # DBヘ接続
        dsn = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        #insert文実行(適宜読み替えてください)
        cur.execute('BEGIN')
        cur.execute("insert into entries values(1,'title', 'body', 'date:XX:YY:ZZ')")
        cur.execute("insert into entries values(2,'title', 'body', 'date:XX:YY:ZZ')")
        # データを取得する
        cur.execute('SELECT * FROM entries')
        for row in cur:
            print(row[0])
        cur.execute('COMMIT')
        exit()        
        
        
    if message.content.startswith("^^getdb "):
        key = message.content.split(" ")[1]
            


 


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
