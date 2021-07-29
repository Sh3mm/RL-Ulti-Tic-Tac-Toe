from typing import List


def linear(size: int, win_state: float) -> List[float]:
    return [(win_state * i) / (size - 1) for i in range(size)]
