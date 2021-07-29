from Arena import Arena
from players import RLPlayer, Random
from NN_learning import BasicNN, linear


def main():
    Arena(
        RLPlayer(BasicNN(), linear), 2,
        [Random()]
    ).train_for(5, 500)


if __name__ == "__main__":
    main()
