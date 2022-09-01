import time
from collections import deque

class Env(object):
    start_time: float
    game_state: bool
    game: object
    msg_dq: deque

    def __init__(self) -> None:
        self.start_time = time.time()
        self.game_state = False
        self.msg_dq = deque()
