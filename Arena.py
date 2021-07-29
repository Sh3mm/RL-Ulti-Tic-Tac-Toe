from typing import List
from datetime import datetime
import json

from players import Player
from game import Game


class Arena:
    def __init__(self, trainee: Player, pos: int, contestants: List[Player]):
        self.trainee = trainee
        self.pos = pos
        self.contestants = contestants

    def train_for(self, round_number: int, steps: int):
        battle_history = []
        for challenger in self.get_challenger(self.contestants, round_number):
            p_1, p_2 = (self.trainee, challenger) if self.pos == 1 else (challenger, self.trainee)
            game = Game(p_1, p_2)
            for _ in range(steps):
                game.start()
                game.reset()

            print(f"results {p_1.get_name()} - {p_2.get_name()}: {game.overall}")
            battle_history.append({"p_1": p_1.get_name(), "p_2": p_2.get_name(), "score": game.overall})

        self.save(battle_history)

    def save(self, battle_history):
        with open(f"battles/RL_{self.trainee.get_name()}_{self.pos}_{datetime.now().strftime('%d_%m_%Y-%H-%M-%S')}",
                  "w") as f:
            json.dump(battle_history, f)
        self.trainee.save(
            f"bots/RL_{self.trainee.get_name()}_{self.pos}_{datetime.now().strftime('%d_%m_%Y-%H-%M-%S')}"
        )

    @staticmethod
    def get_challenger(contestants: List[Player], round_number: int):
        for i in range(round_number):
            for c in contestants:
                yield c
