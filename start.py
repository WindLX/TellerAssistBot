import time
import logging

from core.main import bot
import core.assist.global_var as g

if __name__ == "__main__":
    g._init()
    g.set_value("start_time", time.time())
    logging.basicConfig(level="INFO")
    bot.run()
