import random
from enum import Enum

from core.game.game_object import GameObject


class ActionTypes(Enum):
    scissors = 0
    stone = 1
    paper = 2


class FingerGuess(GameObject):
    player_dict: dict
    game_state: list
    content: list
    is_end: bool

    def __init__(self):
        super().__init__()

    def add_player(self, player_info: list):
        self.player_dict.update({"id": player_info[0]})
        self.player_dict.update({"name": player_info[1]})
        self.player_dict.update({"icon": player_info[2]})
    
    def update_state(self, action: ActionTypes):
        self.game_state.append(random.choice([ActionTypes.scissors, ActionTypes.stone, ActionTypes.paper]))
        self.game_state.append(action)

    def jud_winner(self):
        self.is_end = True
        if self.game_state[1] == self.game_state[0]:
            return 2
        elif self.game_state[1] == ActionTypes.paper:
            if self.game_state[0] == ActionTypes.scissors:
                return 0
            else:
                return 1
        elif self.game_state[1] == ActionTypes.stone:
            if self.game_state[0] == ActionTypes.paper:
                return 0
            else:
                return 1
        else:
            if self.game_state[0] == ActionTypes.stone:
                return 0
            else:
                return 1

    def clear_game(self) -> bool:
        return super().clear_game()
