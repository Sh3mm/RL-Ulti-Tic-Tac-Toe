from typing import List
import random as rd

from game import Board, Move
from players import Player


class Random(Player):
    def __init__(self):
        super().__init__()

    def play(self, board: Board, moves: List[Move], p_number: int) -> Move:
        choice = rd.choice(moves)
        return choice
