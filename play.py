#!/usr/bin/env python3
import signal

from common.logos import logo_game_hub
from treasure_map.play_treasure_map import treasure_map
from rock_paper_scissors_lizard_spock.play_rock_paper_scissors_lizard_spock import rock_paper_scissors_lizard_spock
from blackjack.play_blackjack import blackjack
from hang_non_binary_person.play_hang_non_binary_person import hang_non_binary_person
from brain_quiz.play_brain_quiz import brain_quiz
from utils.functions import _generate_options_for_selection, _single_selection


def goodbye():
    exit("\nGoodbye 👋")


games_list = [("Treasure Map", treasure_map),
              ("Rock Paper Scissors Lizard Spock", rock_paper_scissors_lizard_spock),
              ("Blackjack", blackjack),
              ("Hang Non Binary Person", hang_non_binary_person),
              ("Brain Quiz", brain_quiz),
              ("Exit", goodbye)
              ]


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
