from typing import List
from uuid import uuid4

from players import Player
from game import Game


class Arena:
    def __init__(self, trainee: Player, pos: int, contestants: List[Player]):
        self.trainee = trainee
        self.pos = pos
        self.contestants = contestants

    def train_for(self, round_number: int, steps: int):
        for challenger in self.get_challenger(self.contestants, round_number):
            p_1, p_2 = (self.trainee, challenger) if self.pos == 1 else (challenger, self.trainee)
            game = Game(p_1, p_2)
            for _ in range(steps):
                game.start()
                game.reset()
            print(f"results {p_1.get_name()} - {p_2.get_name()}: {game.overall}")

        self.trainee.save(f"bots/RL_{self.trainee.get_name()}_{self.pos}_{uuid4()}")

    @staticmethod
    def get_challenger(contestants: List[Player], round_number: int):
        for i in range(round_number):
            for c in contestants:
                yield c
