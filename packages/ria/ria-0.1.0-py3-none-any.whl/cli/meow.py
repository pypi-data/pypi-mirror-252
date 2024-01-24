import argparse

from ria.Cat import Cat

DESCRIPTION = "Meow a cat."


def script_entry() -> None:
    """
    The entry point for the ria script.

    :return: None.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-n', '--name', required=True,
        help='The name of the cat.'
    )
    parser.add_argument(
        '-a', '--age', required=False,
        help='The age of the cat in years.'
    )
    parser.add_argument(
        '-c', '--colour', required=False,
        help='The color of the cat\'s fur.'
    )
    parser.add_argument(
        '-t', '--times', type=int, required=False, default=1,
        help='The number of times the cat will meow. Default is 1.'
    )
    args = parser.parse_args()

    Cat(name=args.name, age=args.age, color=args.colour).meow(times=args.times)
