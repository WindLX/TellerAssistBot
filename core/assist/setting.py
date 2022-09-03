import time
from collections import deque

from core.game.game_object import GameObject

class Env(object):
    start_time: float
    msg_dq: deque
    game_state: bool
    game: GameObject
    game_sign: dict

    def __init__(self) -> None:
        self.start_time = time.time()
        self.game_state = False
        self.msg_dq = deque()
        self.game_sign = {}

    def start_game(self, game: GameObject):
        self.game_sign.clear()
        self.game = game
        self.game_state = True

    def add_game_sign(self, key, value):
        self.game_sign.update({key: value})

    def end_game(self):
        self.game_sign.clear()
        self.game_state = False
        self.game.clear_game()
        self.game = None
