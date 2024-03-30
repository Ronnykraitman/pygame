import random

from common.colors import Bright_Cyan, Color_Off
from common.lists import sweet_words
from common.logos import python_name
from simple_term_menu import TerminalMenu


def _switch_user(currently_playing_user, player_external):
    return python_name if currently_playing_user != python_name else player_external

def get_user_name():
    user_name = input(f"What is your name {random.choice(sweet_words)}: ").title()
    while user_name == "Python":
        user_name = input("You can't be Python, don't be sussy. Select a new name: ").title()
    return f"{Bright_Cyan}{user_name}{Color_Off}"

def _single_selection(options: list, title: str) -> int:
    terminal_menu = TerminalMenu(
        options, title=title)
    return terminal_menu.show()

def _generate_options_for_selection(options_list: list):
    """
    :param options_dict: a dict of available user facing methods
    :return: a list of these options, ready for TerminalMenu
    """
    options = []
    size = len(options_list)
    for index in range(size):
        options.append(f"[{index + 1}] - {options_list[index][0]}")
    return options
