from typing import List, Callable
import random as rd

from game import Board, Move
from players import Player
from NN_learning import BasicNN


class RLPlayer(Player):
    def __init__(self, network: BasicNN, reward_dist: Callable[[int, float], List[float]], r_rate=.2):
        super().__init__()
        self.network = network
        self.reward_dist = reward_dist
        self.r_rate = r_rate

    def play(self, board: Board, next_moves: List[Move], p_number: int) -> Move:
        if rd.random() < self.r_rate:
            return rd.choice(next_moves)

        prediction = self.network.predict(
            [board.set_as_temp(move[0], move[1], p_number) for move in next_moves]
        )

        return max(zip(prediction, next_moves), key=lambda x: x[0])[1]

    def update(self, win_state: float, history: List[Move]):
        board = Board()
        boards = [board.set(move[0], move[1], i % 2 + 1, False) for i, move in enumerate(history)]

        scores = self.reward_dist(len(history), win_state)

        self.network.train(boards, scores)

    def save(self, path: str):
        self.network.save(path)

    def load(self, path: str):
        self.network.load(path)

    def get_name(self):
        return f"{self.network.get_name()}_{self.reward_dist.__name__}_{self.r_rate}"
