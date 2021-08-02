from multiprocessing import Pool
import os

from Arena import Arena
from players import RLPlayer, Random
from NN_learning import BasicNN, HiddenNN, linear, root, expo


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def main(elements):
    network, reward, r_rate, act_in, act_out = elements
    Arena(
        RLPlayer(network(act_in, act_out), reward, r_rate), 1,
        [Random()]
    ).train_for(80, 500)


def gen_pos():
    networks = [BasicNN, HiddenNN]
    rewards = [linear, root, expo]
    r_rates = [.1, .5, .2, .3]
    act_ins = ["relu", "sigmoid"]
    act_outs = ["linear", "tanh"]

    for network in networks:
        for reward in rewards:
            for r_rate in r_rates:
                for act_in in act_ins:
                    for act_out in act_outs:
                        yield network, reward, r_rate, act_in, act_out


if __name__ == "__main__":
    pool = Pool(4)
    x = pool.map_async(main, gen_pos())
    x.get()
