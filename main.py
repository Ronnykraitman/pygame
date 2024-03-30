#!/usr/bin/env python3
import signal

from common.logos import logo_game_hub
from treasure_map.play_treasure_map import treasure_map
from rock_paper_scissors_lizard_spock.play_rock_paper_scissors_lizard_spock import rock_paper_scissors_lizard_spock
from blackjack.play_blackjack import blackjack
from utils.functions import _generate_options_for_selection, _single_selection

games_list = [("Treasure Map", treasure_map),
              ("Rock Paper Scissors Lizard Spock", rock_paper_scissors_lizard_spock),
              ("Blackjack", blackjack)
              ]


def goodbye():
    exit("\nGoodbye 👋")


def signal_handler(signal, frame):
    goodbye()


def start():
    menu_options: list = _generate_options_for_selection(games_list)
    index = _single_selection(menu_options, "Available games:")
    games_list[index][1]()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("\nWelcome to the")
    print(logo_game_hub)
    print("🃏🕹️🎱🏓🎳🎲🎮👾🎯🎰🃏🕹️🎱🏓🎳🎲🎮👾🎯🎰🎳🎲🎮👾🎯🎰🃏🕹️🎱🏓🎳🎲🎮👾🎯🎰🃏🕹️🎱🏓🎳🎲🎮👾🎯🎰" + "\n")
    start()
