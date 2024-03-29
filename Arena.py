from typing import List
import json

from players import Player, RLPlayer, Random
from game import Game


class Arena:
    verif = 500
    def __init__(self, trainee: RLPlayer, pos: int, contestants: List[Player], error=.1):
        self.trainee = trainee
        self.pos = pos
        self.contestants = contestants
        self.error = error

    def train_for(self, round_number: int, steps: int):
        best = 0
        game_list = []
        for challenger in self.get_challenger(self.contestants, round_number):
            p_1, p_2 = (self.trainee, challenger) if self.pos == 1 else (challenger, self.trainee)
            game = Game(p_1, p_2)
            for _ in range(steps):
                game.start()
                game_list.append((game.history, game.victor))
                game.reset()

            result = self.test_trainee()["p_1" if self.pos == 1 else "p_2"]
            if result + self.error * self.verif < best:
                self.trainee.load(f"bots/{self.trainee.get_name()}_{self.pos}")

            if (self.verif - best) * .1 < result - best:
                self.trainee.save(f"bots/{self.trainee.get_name()}_{self.pos}")
                best = result

        with open(f"games/{self.trainee.get_name()}_{self.pos}", "w") as f:
            json.dump(game_list, f)

    def test_trainee(self):
        t = self.trainee.r_rate
        self.trainee.r_rate = 0
        p_1, p_2 = (self.trainee, Random()) if self.pos == 1 else (Random(), self.trainee)
        game = Game(p_1, p_2, learn=False)
        for _ in range(self.verif):
            game.start()
            game.reset()

        print(f"results {p_1.get_name()} - {p_2.get_name()}: {game.overall}")
        self.trainee.r_rate = t
        return game.overall


    @staticmethod
    def get_challenger(contestants: List[Player], round_number: int):
        for i in range(round_number):
            for c in contestants:
                yield c
