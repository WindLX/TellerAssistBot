from abc import ABC, abstractmethod
import random

class GameObject(ABC):
    player_dict: dict
    game_state: list
    content: list
    is_end: bool

    def __init__(self) -> None:
        super().__init__()
        self.player_dict = dict()
        self.content = list()
        self.is_end = False
        self.game_state = []
    
    @abstractmethod
    def add_player(self):
        pass
    
    @abstractmethod
    def update_state(self):
        pass

    @abstractmethod
    def jud_winner(self):
        pass

    @abstractmethod
    def clear_game(self) -> bool:
        self.player_dict = dict()
        self.game_state = dict()
        self.content = list()
        self.is_end = False
        return True

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