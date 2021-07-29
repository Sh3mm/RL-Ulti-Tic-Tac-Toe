from typing import Tuple, List

from game import Board, Move
from players import Player


class Game:
    __conv_dict = {-1: "tie", 1: "p_1", 2: "p_2"}

    def __init__(self, player1=None, player2=None, learn=True):
        self.board = Board()
        self.history: List[Move] = []
        self.players: Tuple[Player, Player] = (player1, player2)
        self.learn = learn
        self.overall = {"tie": 0, "p_1": 0, "p_2": 0}

    def start(self):
        win_state = 0
        turn = 0
        while win_state == 0:
            player = self.players[turn % 2]
            moves = self.get_next_moves()
            output = player.play(self.board, moves, (turn % 2) + 1)
            self.board.set(*output, (turn % 2) + 1)
            self.history.append(output)

            win_state = self.board.check_win()
            turn += 1

        self.overall[self.__conv_dict[win_state]] += 1
        self.player_learn(win_state)

    def reset(self):
        self.board = Board()
        self.history = []

    def get_next_moves(self):
        condition = len(self.history) != 0 and self.board.board[self.history[-1][1] // 3][self.history[-1][1] % 3] == 0
        return self.board.get_available(self.history[-1][1]) if condition else self.board.get_available()

    def player_learn(self, win_state):
        if self.learn:
            self.players[0].update(float(1 == win_state) if win_state != -1 else .5, self.history)
            self.players[1].update(float(2 == win_state) if win_state != -1 else .5, self.history)

