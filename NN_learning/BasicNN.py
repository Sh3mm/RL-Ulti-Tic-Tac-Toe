from typing import List

from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, Flatten, InputLayer
import numpy as np

from NN_learning import board_to_1d, board_to_2d
from game import Board


class BasicNN:
    def __init__(self, act_in="relu", act_out="linear"):
        self.act_in = act_in
        self.act_out = act_out
        self.model = self.init_model(act_in, act_out)

    def predict(self, games: List[np.ndarray]):
        input_states = np.asarray([board_to_1d(game).reshape((1, 81)) for game in games])
        chance = self.model(input_states)
        return chance

    def train(self, boards: List[Board], scores: List[float]):
        all_flat_states = [board_to_1d(board.array) for board in boards]

        self.model.fit(
            np.asarray(all_flat_states),
            np.asarray(scores),
            verbose=0
        )

    def load(self, path: str):
        self.model = load_model(path)
        return self

    def save(self, path: str):
        self.model.save(path)

    def get_name(self):
        return f"{type(self).__name__}_{self.act_in}_{self.act_out}"

    @staticmethod
    def init_model(act_in: str, act_out: str):
        model = Sequential()
        model.add(Dense(81, input_dim=81, activation=act_in))
        model.add(Dense(1, activation=act_out, kernel_initializer="glorot_uniform"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model


class HiddenNN(BasicNN):
    @staticmethod
    def init_model(act_in: str, act_out: str):
        model = Sequential()
        model.add(Dense(81, input_dim=81, activation=act_in))
        model.add(Dense(18, activation=act_in))
        model.add(Dense(1, activation=act_out, kernel_initializer="glorot_uniform"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model


class ConvNN(BasicNN):
    def predict(self, games: np.ndarray):
        input_states = np.asarray([board_to_2d(game) for game in games])
        chance = self.model(input_states)
        return chance

    def train(self, boards: List[Board], scores: List[float]):

        all_flat_states = [board_to_2d(board.array) for board in boards]

        self.model.fit(
            np.asarray(all_flat_states),
            np.asarray(scores),
            verbose=0
        )

    @staticmethod
    def init_model(act_in: str, act_out: str):
        model = Sequential()
        model.add(InputLayer(input_shape=(9, 9, 1)))
        model.add(Conv2D(9, 3, activation=act_in))
        model.add(Flatten())
        model.add(Dense(81, activation=act_in))
        model.add(Dense(1, activation=act_out, kernel_initializer="glorot_uniform"))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

