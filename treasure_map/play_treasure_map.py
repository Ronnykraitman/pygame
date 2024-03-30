import random
import sys
from time import sleep

from arts.colors import Bright_Cyan, Color_Off, Yellow
from arts.logos import python_name, python_logo, dots
from prettytable import PrettyTable
import itertools

from utils.functions import _switch_user, _single_selection, get_user_name

the_rules = '''
########################################################################################################
# The rules:                                                                                           #
# Somewhere in the map, there is a hidden golden trophy                                                #
# Your task is simple: select the coordinates that will expose the trophy before Python will           #
########################################################################################################
'''


def _create_selection_options(available_coordinates_as_tuple: list):
    available_coordinates_as_string = []
    for x, y in available_coordinates_as_tuple:
        available_coordinates_as_string.append(x + y)

    return available_coordinates_as_string


def _convert_string_coordinates_to_tuple(coordinates):
    return coordinates[0], coordinates[1]


def play_treasure_map(external_player_name=None):
    if external_player_name is None:
        external_player_name = f"{Bright_Cyan}{get_user_name()}{Color_Off}"
    current_player = external_player_name
    is_treasure_found = False

    table = PrettyTable(title=f"{Yellow}TREASURE MAP{Color_Off}", align="c", padding_width=5, border=False,
                        preserve_internal_border=True)

    x_coordinates = ["A", "B", "C"]
    y_coordinates = ["1", "2", "3"]
    xy_coordinates = [x_coordinates, y_coordinates]

    available_coordinates = list(itertools.product(*xy_coordinates))
    trophy_coordinates: tuple = available_coordinates[random.randint(0, len(available_coordinates) - 1)]

    print("The treasure 🏆 has been hidden.\n")
    empty_columns = ["⬜", "⬜", "⬜"]
    table.add_column("X/Y", x_coordinates)
    table.add_column("1", empty_columns)
    table.add_column("2", empty_columns)
    table.add_column("3", empty_columns)
    print(f"As courtesy, {external_player_name} start first\n")

    options = _create_selection_options(available_coordinates)
    while not is_treasure_found:
        print(table)
        print("\n")
        if current_player == external_player_name:
            index_selection = _single_selection(options, "Available Coordinates")
            selected_coordinates = _convert_string_coordinates_to_tuple(options[index_selection])
            option_to_remove = options[index_selection]
            options.remove(option_to_remove)
        else:
            for i in range(len(dots)):
                sleep(0.5)
                sys.stdout.write("\r" + f"{python_name} {python_logo} is playing" + dots[i])
                sys.stdout.flush()
            print("\n")
            random_selection_index = random.randint(0, len(options) - 1)
            selected_coordinates = _convert_string_coordinates_to_tuple(options[random_selection_index])
            option_to_remove = options[random_selection_index]
            options.remove(option_to_remove)

        if selected_coordinates == trophy_coordinates:
            table._rows[x_coordinates.index(selected_coordinates[0])][int(selected_coordinates[1])] = "🏆"
            print(f"\nOMFG!!! {current_player} found the treasure 🏆, lucky dog\n")
            print(table)
            is_treasure_found = True
            print("\n")
        else:
            table._rows[x_coordinates.index(selected_coordinates[0])][int(selected_coordinates[1])] = "❌"
            current_player = _switch_user(current_player, external_player_name)

    return external_player_name


def treasure_map():
    print("\nWelcome to Find The Treasure 📍")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print(the_rules + "\n")
    stop = False
    external_player_name = play_treasure_map()
    while not stop:
        options = ["Yes", "No - Main Menu"]
        index = _single_selection(options, "Play again?")
        match index:
            case 0:
                play_treasure_map(external_player_name)
            case 1:
                from main import start
                stop = True
                print("\nSee you later 🎯🎯🎯\n")
                start()
