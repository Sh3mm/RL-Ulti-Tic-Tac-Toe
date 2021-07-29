from Arena import Arena
from players import RLPlayer, Random
from NN_learning import BasicNN, HiddenNN, linear, root, expo


def main():
    Arena(RLPlayer(BasicNN(), linear, .1), 1, [Random()]).train_for(120, 500)
    Arena(RLPlayer(HiddenNN(), linear, .1), 2, [Random()]).train_for(120, 500)


if __name__ == "__main__":
    main()
