import os
import json
import random

import core
from khl import Bot, Message


bot = Bot(token=core.get_token())

# /help 指令
@bot.command()
async def help(msg: Message):
    with open('./TellerAssistBot/config/help.txt', 'r', encoding='utf-8')as f:
        data = f.readlines()
    content = ""
    for elements in data:
        content = content + elements
    await msg.reply(content) 


# /hello 指令
@bot.command(name='hello')
async def hello(msg: Message, is_secret: int = 0):
    if is_secret == 1:
        is_secret = True
    else:
        is_secret = False
    await msg.reply(':grinning: Hello! I\'m {name}. Nice to meet you!'.format(name=core.load_information(0, 'name')), is_temp=is_secret)


# /roll 指令
@bot.command()
async def roll(msg: Message, t_min: int, t_max: int, n: int = 1, is_secret: int = 0):
    if is_secret == 1:
        is_secret = True
    else:
        is_secret = False
    if t_min > t_max:
        await msg.reply(':cold_sweat: Sorry, you can\'t set the lower bound on a die higher than its upper bound.')
    result = [random.randint(t_min, t_max) for i in range(n)]
    if t_min >= 0 and t_max <= 10:
        content = ""
        for elements in result:
            content += core.load_str2emoji(0, str(elements))
        await msg.reply(f':partying_face: You got: {content}', is_temp=is_secret)
    else:
        await msg.reply(f':partying_face: You got: {result}', is_temp=is_secret)


# 开始
bot.run()
