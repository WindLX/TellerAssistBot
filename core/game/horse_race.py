import time
import datetime
import random
import pandas as pd

from khl import Channel
from core.assist.read_data import load_horse, load_str2emoji


def random_by_prob(sequence, probability):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(sequence, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

def replace_str_by_index(string, start, end, sub_str):
    ret = string[: start] + sub_str + string[end:]
    return ret

class HorseRace(object):
    horse_dict: pd.DataFrame
    player_dict: dict
    game_state: list
    content: list
    map: list
    is_end: bool

    def __init__(self):
        self.horse_dict = load_horse().sample(n=4, axis=0)
        self.player_dict = {}
        self.game_state = [0] * 4
        self.content = []
        self.map = []
        self.draw_map()
        self.is_end = False

    def add_player(self, player_name:str, horse_name:str):
        self.player_dict.update({player_name: horse_name})
    
    def update_state(self):
        self.content = []
        seq = [-1, 0, 1, 2, 3]
        prob = [0.05, 0.1, 0.6, 0.2, 0.05]
        step = [random_by_prob(seq, prob) for i in range(4)]
        for i in range(len(self.game_state)):
            if step[i] == -1:
                self.content.append(str(self.horse_dict.iloc[i, 0]) + " runs back!")
            if step[i] == 3:
                self.content.append(str(self.horse_dict.iloc[i, 0]) + " lungs forward!")
            self.game_state[i] += step[i]
            if self.game_state[i] <= 0:
                self.game_state[i] = 0
            if self.game_state[i] >= 10:
                self.game_state[i] = 10
                self.is_end = True
                return

    def jud_winner(self):
        d = []
        for i in range(len(self.game_state)):
            if self.game_state[i] == 10:
                d.append(str(self.horse_dict.iloc[i, 0]))                
        return d

    def draw_map(self):
        self.map = []
        line = ""
        road = " " * 50
        for i in range(5):
            line += ":evergreen_tree::deciduous_tree:"
        self.map.append(line)
        for i in range(len(self.game_state)):
            road = replace_str_by_index(road, -5 * (self.game_state[i] + 1), -5 * self.game_state[i], ":racehorse:")
            self.map.append(road)
            road = " " * 50
        self.map.append(line)
