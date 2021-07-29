from typing import List, Tuple
import abc

from game import Board, Move


class Player:
    def __init__(self):
        ...

    @abc.abstractmethod
    def play(self, board: Board, next_moves: List[Move], p_number:int) -> Move:
        ...

    def update(self, win_state: float, history: List[Move]):
        ...

    def save(self, path: str):
        ...

    def get_name(self):
        return str(type(self).__name__)
