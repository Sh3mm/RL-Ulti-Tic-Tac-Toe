from os import listdir, environ
import csv

from players import RLPlayer, Random
from NN_learning import BasicNN
from NN_learning import root, expo, linear
from Arena import Arena

environ['CUDA_VISIBLE_DEVICES'] = '-1'


reward_dict = {root.__name__: root, expo.__name__: expo, linear.__name__: linear}
header = ["model", "act_in", "act_out", "reward_dist", "random_disc", "player", "tie", "win", "loss"]
file = "resutls.csv"


def main():
    bots = listdir("bots/")
    Arena.verif = 1_000

    with open(file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for bot, info in get_bots(bots):
            overall = Arena(bot, 1, [Random()]).test_trainee()
            writer.writerow(info + list(overall.values()))


def get_bots(dirs: list):
    dirs = [d for d in dirs if d.split("_")[0] == "BasicNN"]
    types = [d.split("_") for d in dirs]
    nets = [(BasicNN(act_in, act_out), reward_dict[reward], rand) for (_, act_in, act_out, reward, rand, _) in types]
    for i, (network, reward, rand) in enumerate(nets):
        yield RLPlayer(network.load(f"bots/{dirs[i]}"), reward, .0), types[i]


if __name__ == "__main__":
    main()
