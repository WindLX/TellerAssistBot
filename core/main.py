import time
import datetime
import random

import core.assist.global_var as g
from core.bot import bot
from core.assist.read_data import load_information
from core.assist.read_data import load_str2emoji
from core.message.card import create_help_card
from core.message.card import create_div_card

from khl import Message

### dialog ###
# /hello
@bot.command(name="hello")
async def hello(msg: Message, is_secret: int = 0):
    if is_secret == 1:
        is_secret = True
    else:
        is_secret = False
    name = load_information('name')
    await msg.reply(f':grinning: Hello! I\'m {name}. Nice to meet you!', is_temp=is_secret)

### tools ###
# /help
@bot.command(name="help")
async def help(msg: Message):
    content = create_help_card()
    await msg.ctx.channel.send(content) 

# /runtime
@bot.command(name="runtime")
async def runtime(msg: Message):
    delta_t = time.time() - g.get_value("start_time")
    t_m,t_s = divmod(delta_t, 60)   
    t_h,t_m = divmod(t_m, 60)
    r_t = ''
    if t_h != 0:
        r_t += "**" + str(int(t_h)) + "** h "
    if t_m != 0:
        r_t += "**" + str(int(t_m)) + "** m "
    if t_s != 0:
        r_t += "**" + str(int(t_s)) + "** s "
    extra = random.choice([" :muscle: I'm still full of energy.", " :fish: Slack off for a while~", " :running_woman: Run le~"])
    content = f":woman_technologist: I've been working for {r_t}." + extra
    await msg.reply(content)

# /time
@bot.command(name="time")
async def get_time(msg: Message):
    now_t = time.strftime('%Y-%m-%d  %H\:%M\:%S', time.localtime())
    content = ":alarm_clock: " + str(now_t)
    await msg.reply(content)

### game ###
# /roll
@bot.command(name="roll")
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
            content += load_str2emoji(0, str(elements))
        await msg.reply(f':partying_face: You got: {content}', is_temp=is_secret)
    else:
        await msg.reply(f':partying_face: You got: {result}', is_temp=is_secret)

# /divine
@bot.command(name="divine")
async def divine(msg: Message, is_secret: int = 0):
    if is_secret == 1:
        is_secret = True
    else:
        is_secret = False
    end_time = datetime.datetime.today()
    start_time = datetime.datetime.strptime(load_information("time_seed"), '%Y-%m-%d')
    delta_t = (end_time - start_time).days
    random.seed(str(delta_t) + str(msg.author.id))
    result = random.randint(0, 43)
    content = create_div_card(result, msg.author.username)
    await msg.reply(content=content, is_temp=is_secret)
