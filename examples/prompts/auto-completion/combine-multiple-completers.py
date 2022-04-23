#!/usr/bin/env python
"""
Example of multiple individual completers that are combined into one.
"""


from quo.completion import WordCompleter, merge_completers
from quo.prompt import Prompt


animal_completer = WordCompleter(
    [
        "alligator",
        "ant",
        "ape",
        "bat",
        "bear",
        "beaver",
        "bee",
        "bison",
        "butterfly",
        "cat",
        "chicken",
        "crocodile",
        "dinosaur",
        "dog",
        "dolphin",
        "dove",
        "duck",
        "eagle",
        "elephant",
        "fish",
        "goat",
        "gorilla",
        "kangaroo",
        "leopard",
        "lion",
        "mouse",
        "rabbit",
        "rat",
        "snake",
        "spider",
        "turkey",
        "turtle",
    ],
    ignore_case=True,
)

color_completer = WordCompleter(
    [
        "red",
        "green",
        "blue",
        "yellow",
        "white",
        "black",
        "orange",
        "gray",
        "pink",
        "purple",
        "cyan",
        "magenta",
        "violet",
    ]
)

session = Prompt()

def main():
    completer = merge_completers([animal_completer, color_completer])

    text = session.prompt(
        "Give some animals: ", completer=completer, complete_while_typing=False
    )
    print("You said: %s" % text)


if __name__ == "__main__":
    main()
