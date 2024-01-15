#導入 Discord.py
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
import urllib.request
import time
import math
import tracemalloc

tracemalloc.start()

# 導入隨機數套件
import random

#為了asyncio.sleep()
import asyncio

# 取得環境設定
load_dotenv()
DISCORD_TOKEN = os.getenv("MTE5NTAwOTQ5MDIxOTcwNDM4Mg.GBGfIU.6Th_lUP4PhUPmKBIbvo9QMhl7_HXTULEGixZ94")

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='!', intents=intents)


#機器人狀態
@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')
    game = discord.Game('プロセカ')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.idle, activity=game)
    

@bot.event
async def on_member_join(member):
    # 當有成員加入伺服器時觸發
    channel = discord.utils.get(member.guild.text_channels, name="一般")  # 替換成你希望發送歡迎訊息的頻道名稱
    if channel:
        await channel.send(f'歡迎 {member.mention} 加入了伺服器！')

@bot.event
async def on_member_remove(member):
    # 當有成員離開伺服器時觸發
    channel = discord.utils.get(member.guild.text_channels, name="一般")  # 替換成你希望發送告別訊息的頻道名稱
    if channel:
        await channel.send(f'我們摯愛的 {member.display_name} 離開了我們，\n於今日悄悄的離開這個普羅圈，我們痛徹心扉，\n就僅僅一眨眼的時間，天人永隔。\n{member.display_name} 安祥的走完了這幾年的音遊旅程，\n他彷彿在沉睡中做了一個美夢。\n夢醒了，留下陪伴我們成長過程中的點點滴滴，\n留下我們永恆的追思與感恩。')


#編輯
@bot.event 
async def on_message_edit(before, after):
  print(before)
  print(after)
  channel = bot.get_channel(1195008346537869363)
  await channel.send(f'太過分了，{ before.author.mention }偷偷把「{before.content}」改成「{after.content}」啦!')

#刪除
@bot.event 
async def on_message_delete(message):
  print(message)
  channel = bot.get_channel(message.channel.id)
  await channel.send(f'太過分了，{ message.author.mention }偷偷刪除了「{message.content}」啦! ')
  return


@bot.event 
#打招呼
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('打招呼'):
        channel = message.channel
        #機器人叫你先跟他說你好
        await channel.send('那你先跟我說你好')
		#檢查函式，確認使用者是否在相同頻道打上「你好」
        def checkmessage(m):
            return m.content == '你好' and m.channel == channel
		#獲取傳訊息的資訊(message是類型，也可以用reaction_add等等動作)
        msg = await client.wait_for('message', check=checkmessage)
        await channel.send('嗨, {.author}！'.format(msg))

#我好帥喔
    if message.content == '我好帥喔':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await message.channel.send('你確定你帥嗎？')

#繪名     
    #如果包含 A，機器人回傳 B
    if message.content == '繪名':
        await message.channel.send('最愛自拍了！')
#彰人
    if message.content == '世界上最討厭的人是誰':
        await message.channel.send('東雲彰人')

#說
    if message.author == client.user:
        return
    #如果以「說」開頭
    if message.content.startswith('說'):
      #分割訊息成兩份
      tmp = message.content.split(" ",2)
      #如果分割後串列長度只有1
      if len(tmp) == 1:
        await message.channel.send("你要我說什麼啦？")
      else:
        await message.channel.send(tmp[1])
    if message.content.startswith('更改狀態'):
        #切兩刀訊息
        tmp = message.content.split(" ",2)
        #如果分割後串列長度只有1
        if len(tmp) == 1:
            await message.channel.send("你要改成什麼啦？")
        else:
            game = discord.Game(tmp[0])
            #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
            await client.change_presence(status=discord.Status.idle, activity=game)

#!roll
    # 預設錯誤訊息
    error = []
    # 處理輸入文字
    content = message.content.replace(' ', '').lower()
    # 如果是「!roll」開頭的訊息
    if message.content.startswith('!roll'):
        content = content.replace('!roll', '')
        # 骰子數量計算
        dice_cont = content.split('d')[0]
        try:
            dice_cont = int(dice_cont)
        except ValueError:
            error.append('How many dice you roll must be an interger!')

        # 骰子類型判斷
        content = content.split('d')[1]
        dice_type = content.split('>')[0]
        try:
            dice_type = int(dice_type)
        except ValueError:
            error.append('Dice type must be an interger!')

        # 成功判斷
        if '>' in content:
            success = content.split('>')[1]
            try:
                success = int(success)    
            except ValueError:
                error.append('Success condition must be an interger!')

        else:
            success = 0
        if len(error) == 0:
            success_count = 0
            result_msg = ''

            # 擲骰子
            results = [random.randint(1, dice_type) for _ in range(dice_cont)]

            for result in results:
                if success > 0 and result >= success:
                    success_count += 1
                result_msg += f'`{result}`, '
            
            await message.channel.send(result_msg)

            if success > 0:
                await message.channel.send(f'Success: `{success_count}`')
        else:
            await message.channel.send(error)

    if message.author == bot.user:
        return
#!team
    if message.content.startswith('!team'):
        await message.channel.send("倍率公式為： \n1 + 隊長技能a% \n+(隊員1號技能b%×0.2) \n+(隊員2號技能c%×0.2) \n+(隊員3號技能d%×0.2) \n+(隊員4號技能e%×0.2)")
        await asyncio.sleep(2)
        await message.channel.send("請輸入技能百分比（格式：a,b,c,d,e）：")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            skills = [float(skill) for skill in msg.content.split(",")]

            result = round(1 + skills[0] * 0.01 + sum(skill * 0.2 * 0.01 for skill in skills[1:]) ,2)

            await message.channel.send(f'計算結果為：{result}')
        except asyncio.TimeoutError:
            await message.channel.send('操作超時，請重新輸入')

#!help   
    if message.content.startswith('!help'):
        await message.channel.send("**`!team`** 可以查詢隊伍加成 \n**`!roll`** **a**d**b** 可以擲骰子(ex.5d10) \n:a:幾個骰子,:b:數字多少以內 a跟b都是數字 \n**`!hentai`** 懂得都懂 \n**`繪名`** 她會回你 \n**`說 OO`** 繪名她會說OO \n**`我好帥喔`** 繪名會嗆你 \n**`打招呼`** 繪名會跟你打招呼 \n**`世界上最討厭的人是誰`**")

#!hentai
    if message.content.startswith('!hentai'):
        first_digit = str(random.randint(0, 4))
        second_digit = str(random.randint(0, 9))
        remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))

    if first_digit == '0':
        result = second_digit + remaining_digits
    else:
        result = first_digit + second_digit + remaining_digits
    result = min(int(result), 491567)

    await message.channel.send("今日本子番號為：")
    await asyncio.sleep(1)
    await message.channel.send(f"nhentai.net/g/{result}/1")



# 在異步上下文中運行機器人
async def main():
    await bot.start('MTE5NTAwOTQ5MDIxOTcwNDM4Mg.GBGfIU.6Th_lUP4PhUPmKBIbvo9QMhl7_HXTULEGixZ94')

# 使用 asyncio 開啟一個新的執行緒保持連接
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# 在異步上下文中運行機器人
if __name__ == "__main__":
    asyncio.run(main())