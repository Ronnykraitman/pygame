from arts.colors import Bright_Cyan, Color_Off, Bright_Magenta
from arts.logos import python_name
from rock_paper_scissors_lizard_spock.art import rock, paper, scissors, lizard, spock, logo_3, logo_2, logo_1
import random
import sys
from time import sleep

from utils.functions import get_user_name, _single_selection

the_rules = '''
########################################################################################################
# The rules are simple as that:                                                                        #
# Scissors cuts Paper => Paper covers Rock                                                             #
# Rock crushes Lizard => Lizard poisons Spock                                                          #
# Spock smashes Scissors => Scissors decapitates Lizard                                                #
# Lizard eats Paper => Paper disproves Spock                                                           #
# Spock vaporizes Rock => And as it always has - Rock crushes Scissors                                 #
########################################################################################################
'''

options_as_tuple = [("Rock", rock), ("Paper", paper), ("Scissors", scissors), ("Lizard", lizard), ("Spock", spock)]


def _create_selection_options_from_tuple(options_as_tuple: list):
    available_options_as_string = []
    for t in options_as_tuple:
        available_options_as_string.append(t[0])

    return available_options_as_string


def __select_winner(player_move, python_move, player_name):
    if player_move[0] == python_move[0]:
        return "Tie"

    match player_move[0]:
        case "Rock":
            if python_move[0] == "Lizard" or python_move[0] == "Scissors":
                return player_name

        case "Paper":
            if python_move[0] == "Rock" or python_move[0] == "Spock":
                return player_name

        case "Scissors":
            if python_move[0] == "Lizard" or python_move[0] == "Paper":
                return player_name

        case "Lizard":
            if python_move[0] == "Spock" or python_move[0] == "Paper":
                return player_name

        case "Spock":
            if python_move[0] == "Scissors" or python_move[0] == "Rock":
                return player_name

    return python_name


def count_to():
    count_numbers = [logo_3, logo_2, logo_1]
    print("Are you ready?\n")
    for n in count_numbers:
        sleep(0.8)
        sys.stdout.write("\r" + n)
        sys.stdout.flush()
    sleep(0.8)
    print("\n")


def play_rock_paper_scissors_lizard_spock(external_player_name=None):

    if external_player_name is None:
        external_player_name = f"{Bright_Cyan}{get_user_name()}{Color_Off}"

    options_as_string = _create_selection_options_from_tuple(options_as_tuple)

    index_selection = _single_selection(options_as_string, "Available Moves")
    external_player_move = options_as_tuple[index_selection]
    python_player_move = options_as_tuple[random.randint(0, len(options_as_tuple) - 1)]

    print(f"{external_player_name}'s move is: {Bright_Magenta}{external_player_move[0]}{Color_Off}")
    print(external_player_move[1] + "\n")
    count_to()
    print(f"\n{python_name}'s move is: {Bright_Magenta}{python_player_move[0]}{Color_Off}")
    print(python_player_move[1] + "\n")

    winner = __select_winner(external_player_move[0], python_player_move[0], external_player_name)
    if winner == "Tie":
        print("It's a Tie. Good game")
    else:
        print(f"The winner is: {winner}. Congrats!\n")
    return external_player_name


def rock_paper_scissors_lizard_spock():
    print("\nWelcome to Rock Paper Scissors Lizard Spock 🖖")
    print("##############################################")
    print(the_rules + "\n")
    stop = False
    external_player_name = play_rock_paper_scissors_lizard_spock()
    while not stop:
        options = ["Yes", "No - Main Menu"]
        index = _single_selection(options, "Play again?")
        match index:
            case 0:
                play_rock_paper_scissors_lizard_spock(external_player_name)
            case 1:
                from main import start
                stop = True
                print("\nSee you later 🎲🎲🎲\n")
                start()
