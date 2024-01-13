#導入 Discord.py
import discord
import time
#為了asyncio.sleep()
import asyncio
#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    game = discord.Game('自拍')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_message(message):
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

    if message.content == '我好帥喔':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await message.channel.send('你確定你帥嗎？')
        #停頓3秒
        await asyncio.sleep(3)
        #刪除訊息
        await tmpmsg.delete()
        
    if message.author == client.user:
        return
    #如果包含 A，機器人回傳 B
    if message.content == '繪名':
        await message.channel.send('最愛自拍了！')

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
            game = discord.Game(tmp[1])
            #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
            await client.change_presence(status=discord.Status.idle, activity=game)
    if message.content == '倍率公式':
        await message.channel.send('倍率公式為： \n1 + a：隊長技能% \n+b：(隊員1號技能%×0.2) \n+c：(隊員2號技能%×0.2) \n+d：(隊員3號技能%×0.2) \n+e：(隊員4號技能%×0.2)')
        await asyncio.sleep(1)
        await message.channel.send('請輸入數字 (格式 a,b,c,d,e)')
        a = input('請輸入數字 ( 格式 a,b,c... )：')   # 新增變數 a，內容是使用者輸入的多個數字，數字以逗號分隔
        b = a.split(',')      # 新增變數 b，內容使用 split 根據逗號將數字拆開為串列
        output = 0            # 設定 output 從 0 開始
        for i in b:           # 使用 for 迴圈，依序取出 b 串列的每個項目
            output += int(i)  # 將 output 的數值加上每個項目 ( 使用 int 將項目轉換成數字 )

print(f'數字總和為：{output}')
     

client.run('MTE5NTc2NDk1MDc3MDEyNjg0OA.GY8lWm.a9Jofeq0lN6pnq23Tha6ujmyhUVvaAh1i2UXog') #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面