import pandas as pd

from core.game.game_object import GameObject, random_by_prob, replace_str_by_index
from core.assist.read_data import load_horse

class HorseRace(GameObject):
    horse_dict: pd.DataFrame
    player_dict: dict
    game_state: list
    content: list
    map: list
    is_end: bool

    def __init__(self):
        super().__init__()
        self.horse_dict = load_horse().sample(n=4, axis=0)
        self.game_state = [0] * 4
        self.map = list()
        self.draw_map()

    def add_player(self, player_name:str, horse_name:str):
        self.player_dict.update({player_name: horse_name})
    
    def update_state(self):
        self.content = list()
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
        d = list()
        for i in range(len(self.game_state)):
            if self.game_state[i] == 10:
                d.append(str(self.horse_dict.iloc[i, 0]))                
        return d

    def clear_game(self):
        self.map.clear()
        self.horse_dict = pd.DataFrame()
        return super().clear_game()

    def draw_map(self):
        self.map = list()
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
