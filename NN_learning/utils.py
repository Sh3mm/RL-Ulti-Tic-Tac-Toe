import numpy as np

from game import Board


def board_to_1d(board: np.ndarray) -> np.ndarray:
    return board.flatten()


def board_to_2d(board: np.ndarray) -> np.ndarray:
    buffer = []
    for i in range(3):
        for j in range(3):
            buffer.append(np.append(board[3 * i][j], [board[3 * i + 1][j], board[3 * i + 2][j]]))
    return np.asarray(buffer).reshape((9, 9, 1))


if __name__ == "__main__":
    b = Board()
    for i in range(9):
        b.set(i, 4, i + 1)
    print(board_to_2d(b.board))
