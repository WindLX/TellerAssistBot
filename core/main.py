import time
import datetime
import random
import asyncio

from core.bot import bot, env
from core.assist.read_data import load_information, load_str2emoji
from core.message.card import create_help_card, create_div_card, create_hrace_card, draw_hrace_card, create_fguess_card
from core.game.horse_race import HorseRace
from core.game.finger_guess import FingerGuess, ActionTypes

from khl import Bot
from khl import Message
from khl import Event, EventTypes

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
    delta_t = time.time() - env.start_time
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

# /exit
@bot.command(name='exit')
async def bot_exit(msg: Message):
    await msg.ctx.channel.send(":kissing_heart: See you next time~")
    tasks = asyncio.Task.all_tasks()
    group = asyncio.gather(*tasks, return_exceptions=True)
    group.cancel()
    bot.loop.run_until_complete(group)
    bot.loop.close()

### game ###
# /roll
@bot.command(name="roll", prefixes=['.'])
async def roll(msg: Message, t_min: int, t_max: int, n: int = 1, is_secret: int = 0):
    if is_secret == 1:
        is_secret = True
    else:
        is_secret = False
    if t_min > t_max:
        await msg.reply(':cold_sweat: Sorry, you can\'t set the lower bound on a die higher than its upper bound.')
    result = [random.randint(t_min, t_max) for i in range(n)]
    if t_min >= 0 and t_max <= 9:
        content = ""
        for elements in result:
            content += load_str2emoji(0, str(elements))
        await msg.reply(f':partying_face: You got: {content}', is_temp=is_secret)
    else:
        await msg.reply(f':partying_face: You got: {result}', is_temp=is_secret)

# /divine
@bot.command(name="divine", prefixes=['.'])
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

# /horse race
@bot.command(name="hrace", prefixes=['.'])
async def horse_race(msg: Message):
    if env.game_state == False:
        env.start_game(HorseRace())
        env.add_game_sign("is_running", False)
        content, end_t = create_hrace_card(env.game.horse_dict)
        ct = draw_hrace_card(env.game.map, env.game.content)
        
        await msg.ctx.channel.send(content)
        time.sleep((end_t - datetime.datetime.now()).total_seconds())
        await msg.ctx.channel.send(ct)
        env.add_game_sign("is_running", True)
        time.sleep(3)

        while True:
            env.game.update_state()
            env.game.draw_map()
            ct = draw_hrace_card(env.game.map, env.game.content)
            await msg.ctx.channel.send(ct)
            time.sleep(3)
            if env.game.is_end:
                break
            
        d = env.game.jud_winner()
        for ele in d:
            ct = f":partying_face: {ele} wins the race! "
            for key, value in env.game.player_dict.items():
                if value == ele:
                    ct += f"@{key} "
        await msg.ctx.channel.send(ct)
        env.end_game()
    else:
        await msg.reply(":cold_sweat: I'm sorry, a game has begun")

# /finger-guessing
@bot.command(name='fguess', prefixes=['.'])
async def finger_guess(msg: Message):
    if env.game_state == False:
        env.start_game(FingerGuess())
        env.add_game_sign("msg_id", msg.id)
        env.add_game_sign("u_name", msg.author.username)
        u_info = [msg.author.id, msg.author.username, msg.author.avatar]
        bot_all_info = await bot.client.fetch_me(True)
        b_info = [bot_all_info.id, bot_all_info.username, bot_all_info.avatar]
        env.add_game_sign("b_name", bot_all_info.username)
        cm = create_fguess_card(bot_info=b_info, player_info=u_info)
        env.game.add_player(u_info)
        await msg.ctx.channel.send(cm)
        await bot.client.add_reaction(msg, "✌")
        await bot.client.add_reaction(msg, "👊")
        await bot.client.add_reaction(msg, "🖐")
    else:
        await msg.reply(":cold_sweat: I'm sorry, a game has begun")

# Handle the +1 to the horse race
@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def hrace_plus(b: Bot, event: Event):
    channel = await b.fetch_public_channel(event.body['target_id'])
    if env.game_state == True and isinstance(env.game, HorseRace) and env.game_sign["is_running"] == False:
        user_name = event.body['user_info']['username']
        horse_name = env.game.horse_dict.iloc[int(event.body['value']), 0]
        if not user_name in env.game.player_dict:
            env.game.add_player(user_name, horse_name)
            await b.client.send(channel, f'@{user_name} chooses {horse_name}')
    elif env.game_sign["is_running"] == True:
        await b.client.send(channel, 'Sorry, the game started.')
    else:
        await b.client.send(channel, 'Sorry, the game finished.')

# Handle the reaction in finger-guessing
@bot.on_event(EventTypes.ADDED_REACTION)
async def fguess_reaction(b: Bot, event: Event):
    if env.game_state:
        if event.body['msg_id'] == env.game_sign['msg_id'] and event.body['user_id'] == env.game.player_dict['id']:
            channel = await b.fetch_public_channel(event.body['channel_id'])
            if event.body["emoji"]["name"] == "✌":
                dm = "✌"
                env.game.update_state(ActionTypes.scissors)
            elif event.body["emoji"]["name"] == "👊":
                dm = "👊"
                env.game.update_state(ActionTypes.stone)
            elif event.body["emoji"]["name"] == "🖐":
                dm = "🖐"
                env.game.update_state(ActionTypes.paper)
            else:
                return
            r = env.game.jud_winner()
            am = env.game_sign["b_name"]
            cm = env.game_sign["u_name"]
            m = env.game.game_state[0]
            if m == ActionTypes.scissors:
                bm = "✌"
            elif m == ActionTypes.paper:
                bm = "🖐"
            else:
                bm = "👊"
            await b.client.send(channel, f"{am} choose {bm}, {cm} choose {dm}.")
            if r == 0:
                await b.client.send(channel, f":partying_face: Winner is {am}!")
            elif r == 1:
                await b.client.send(channel, f":partying_face: Winner is {cm}!")
            else:
                await b.client.send(channel, ":partying_face: We're tied~")
            env.end_game()
