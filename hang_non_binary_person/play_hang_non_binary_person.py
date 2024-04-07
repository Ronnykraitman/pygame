import random
import re
from time import sleep

from common.colors import Bright_Red, Color_Off, Bright_Yellow
from common.lists import letters_list
from common.logos import python_name
from hang_non_binary_person.art import non_binary_person_stages
from utils.functions import get_user_name, _switch_user, _single_selection

allowed_guesses = 10
letters_for_python = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                      't', 'u', 'v', 'w', 'x', 'y', 'z']

letters_used = []

the_rules = '''
########################################################################################################
# The rules are simple. You have 10 guesses. Combined.                                                 #
# If you get a letter right, you keep going. If not, the turn moves to the next player.                #
# The winner - the one that was not responsible to the final hit that killed the non binary person     #
########################################################################################################
'''


def select_random_word() -> str:
    words = []
    with open('/usr/share/dict/words') as f:
        for line in f:
            words.append(line.strip())
    word = random.choice(words)
    return word


def check_if_alpha(letter: str):
    return True if letter in letters_list else False

def check_if_used(letter: str):
    return True if letter in letters_used else False
def get_letter_from_user(player_name):
    global letters_used
    global letters_for_python
    letter = input(f"OK {player_name}, guess a letter: ").lower()
    is_abc = check_if_alpha(letter)
    is_used = check_if_used(letter)

    while not is_abc or is_used:
        letter = input(
            f"The letter {Bright_Red}{letter}{Color_Off} is either used already or not in English. Choose again: ")
        is_abc = check_if_alpha(letter)
        is_used = check_if_used(letter)

    letters_used.append(letter)
    letters_for_python.remove(letter)
    return letter


def check_letter_exist_in_the_word(word: str, letter: str):
    indexes = [match.start() for match in re.finditer(letter.lower(), word)]
    return indexes


def generate_blank_word_as_list(word_length):
    blank = []
    for i in range(0, word_length):
        blank.append(' ⬜ ')
    return blank


def play_hang_non_binary_person(external_player_name=None):
    global letters_used
    global letters_for_python
    wrong_guesses = 0
    guesses = 0
    selected_word = select_random_word()
    guesses_needed = len(set(selected_word))
    blank_word_as_list = generate_blank_word_as_list(len(selected_word))
    if external_player_name is None:
        external_player_name = get_user_name()

    print(
        f"\nYou have {len(selected_word)} letters word to guess before killing the non binary person: {"".join(blank_word_as_list)}\n")

    print(f"As courtesy, {external_player_name} start first\n")
    currently_playing_user = external_player_name

    while wrong_guesses < allowed_guesses:
        if currently_playing_user == external_player_name:
            letter_from_player = get_letter_from_user(currently_playing_user)
        else:
            letter_from_player = random.choice(letters_for_python)
            letters_used.append(letter_from_player)
            letters_for_python.remove(letter_from_player)
            print(f"{python_name} chose the letter: {Bright_Yellow}{letter_from_player.upper()}{Color_Off}")

        indexes = check_letter_exist_in_the_word(selected_word, letter_from_player)
        if indexes:
            guesses += 1
            for index in indexes:
                blank_word_as_list[index] = f"{Bright_Yellow}{selected_word[index].upper()}{Color_Off}"
                if guesses == guesses_needed:
                    print(f"\nOMG {currently_playing_user} - saved the non binary person and WON !!!\n")
                    print("Good game\n")
                    return external_player_name

            print(f"\nGetting closer: {"".join(blank_word_as_list)}\n")
            sleep(1)
        else:
            sleep(1)
            print("Oh no.. you got it wrong. The non binary is one step closer to death!\n")
            print(non_binary_person_stages[wrong_guesses] + "\n")
            wrong_guesses += 1
            if wrong_guesses == allowed_guesses:
                print(f"\n{currently_playing_user} - You killed the non binary person!! How could you?\n")
                print(f"BTW - the word was: {selected_word}")
                return external_player_name
            if wrong_guesses != allowed_guesses:
                currently_playing_user = _switch_user(currently_playing_user, external_player_name)
                print(f"Now its {currently_playing_user}'s turn\n")


def hang_non_binary_person():
    print("\nWelcome to the Hangman game\n ")
    print(the_rules + "\n")
    stop = False
    external_player_name = play_hang_non_binary_person()
    while not stop:
        options = ["Yes", "No - Main Menu"]
        index = _single_selection(options, "Play again?")
        match index:
            case 0:
                play_hang_non_binary_person(external_player_name)
            case 1:
                from play import start
                stop = True
                print("\nSee you later 🎳🎳🎳\n")
                start()
