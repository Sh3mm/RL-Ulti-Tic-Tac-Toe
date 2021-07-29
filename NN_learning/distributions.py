from typing import List
from math import sqrt


def linear(size: int, win_state: float) -> List[float]:
    return [(win_state * i) / size for i in range(size)]


def expo(size: int, win_state: float) -> List[float]:
    return [((win_state * i) / size)**3 for i in range(size)]


def root(size: int, win_state: float) -> List[float]:
    return [win_state * sqrt((win_state * i) / size) for i in range(size)]
