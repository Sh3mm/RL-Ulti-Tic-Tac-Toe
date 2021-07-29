import itertools
from typing import NewType, Tuple

import numpy as np
from termcolor import colored


Move = NewType('Move', Tuple[int, int])


class Board:
    def __init__(self):
        self.array = np.zeros(shape=(9, 3, 3))
        self.board = np.zeros(shape=(3, 3))

    def set(self, game, tile, player, check=True):
        self.array[game][tile // 3][tile % 3] = player
        if check:
            self.board[game // 3][game % 3] = self.check_win(game)
        return self

    def set_as_temp(self, game, tile, player) -> np.ndarray:
        temp = self.array.copy()
        temp[game][tile // 3][tile % 3] = player
        return temp

    def check_win(self, game=None):
        game = self.array[game] if game is not None else self.board

        for row in list(game) + list(game.transpose()) + [game.diagonal(), np.fliplr(game).diagonal()]:
            if len(set(row)) == 1 and list(set(row))[0] != 0:
                return list(set(row))[0]
        if np.count_nonzero(game) == 9:
            return -1
        return 0

    def get_available(self, game=None):
        if game is None:
            won = [i for i in range(9) if self.check_win(i) == 0]
            return list(itertools.chain(*[self.get_available(x) for x in won]))

        x, y = np.where(self.array[game] == 0)
        return list(zip([game] * x.size, 3 * x + y))

    def __str__(self):
        buffer: str = ""

        for i in range(3):
            for j in range(3):
                buffer += f"{self.array[3 * i][j]}‖{self.array[3 * i + 1][j]}‖{self.array[3 * i + 2][j]}\n"\
                    .replace("1", colored("1", "red")).replace("2", colored("2", "green"))
            buffer += "-------------------------------\n" if i != 2 else ""

        return buffer
