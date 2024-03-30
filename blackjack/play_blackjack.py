import random
from time import sleep
from blackjack.art import card_deck_suits, court_cards
from common.colors import Bright_Cyan, Color_Off
from common.logos import python_name
from utils.functions import get_user_name, _single_selection

used_cards = []

the_rules = '''
########################################################################################################
# The rules:                                                                                           #
# You and Python both get two cards for start, You can see only one of Python's cards                  #
# Your goal: Get to 21                                                                                 #
# You can ask 'Hit' and get another card from the deck or 'Stay' to stop the round                     #
# If you got more than 21, its a Bust, and you lose, If Python got more than 21, You win.              #
# If neither of you got 21, the closest one of you is the winner                                       #
# Betting on money is coming soon. You can practice till then                                          #
########################################################################################################
'''

def get_card(cards_deck: list):
    global used_cards
    card = random.choice(cards_deck)

    while card in used_cards:
        card = random.choice(cards_deck)

    used_cards.append(card)
    return card


def calculate_score(card: tuple, total_score: int):
    if str(card[0]).isnumeric():
        return total_score + card[0]
    elif card[0] == "K" or card[0] == "Q" or card[0] == "J":
        return total_score + 10
    elif card[0] == "A":
        if total_score <= 10:
            return total_score + 11
        else:
            return total_score + 1


def check_winner(player_score, python_score, external_player_name, player_cards, python_cards):

    player_diff = abs(21 - player_score)
    python_diff = abs(21 - python_score)

    print_game_hands(python_cards, external_player_name, player_cards, player_score)

    if player_diff == python_diff:
        return "It's a TIE"
    elif player_diff > python_diff:
        return python_name
    return external_player_name


def print_player_hand(player_cards: list):
    print()
    handSize = len(player_cards)
    print('┌───────┐ ' * handSize)
    for card in player_cards:
        print(f'| {card[0]:<2}    | ', end='')
    print('\n' + '|       | ' * handSize)
    for card in player_cards:
        print(f'|   {card[1]}   | ', end='')
    print('\n' + '|       | ' * handSize)
    for card in player_cards:
        print(f'|    {card[0]:>2} | ', end='')
    print('\n' + '└───────┘ ' * handSize)
    print()


def print_game_hands(python_cards, external_player_name, player_cards, player_score):
    print("\n=>=>=>=>=>=>=>=> PLAYERS HAND STATUS =>=>=>=>=>=>=>=>\n")
    print(f"{python_name}'s hand")
    print_player_hand(python_cards)
    print()
    print(f"{external_player_name}'s hand with score of {player_score}")
    print_player_hand(player_cards)
    print("\n<=<=<=<=<=<=<=<= PLAYERS HAND STATUS <=<=<=<=<=<=<=<=\n")


def check_player_bust_or_clean_win(player_score, external_player_name, player_cards, python_cards):
    if player_score == 21:
        print_game_hands(python_cards, external_player_name, player_cards, player_score)
        print(f"Sorry {python_name}, {external_player_name} has a clean win\n")
        return external_player_name
    if player_score > 21:
        print_game_hands(python_cards, external_player_name, player_cards, player_score)
        print(f"Sorry {external_player_name}, it's a BUST")
        print(f"The winner is {python_name} !!!!\n")
        return external_player_name
    return None

def play_blackjack(external_player_name=None):

    if external_player_name is None:
        external_player_name = f"{Bright_Cyan}{get_user_name()}{Color_Off}"

    cards_deck = []
    for suit in card_deck_suits:
        for n in range(2, 11):
            cards_deck.append((n, suit))
        for cc in court_cards:
            cards_deck.append((cc, suit))

    tokens = ["1", "5", "25", "50", "100", "500", "1000"]

    player_cards = []
    python_cards = []
    player_score = 0
    python_score = 0
    player_money = 1000
    blackjack_winner = None
    cards_array = []
    blackjack_moves = ["Hit", "Stay"]

    for i in range(2):
        card = get_card(cards_deck)
        player_score = calculate_score(card, player_score)
        player_cards.append(card)
        card = get_card(cards_deck)
        python_score = calculate_score(card, python_score)
        python_cards.append(card)

    print_game_hands([python_cards[0]], external_player_name, player_cards, player_score)

    blackjack_winner = check_player_bust_or_clean_win(player_score, external_player_name, player_cards, python_cards)

    move = blackjack_moves[_single_selection(blackjack_moves, "Your next move:")]
    while blackjack_winner is None and move == "Hit":
        card = get_card(cards_deck)
        player_score = calculate_score(card, player_score)
        player_cards.append(card)
        blackjack_winner = check_player_bust_or_clean_win(player_score, external_player_name, player_cards, python_cards)

        if not blackjack_winner:
            print_game_hands([python_cards[0]], external_player_name, player_cards, player_score)
            move = blackjack_moves[_single_selection(blackjack_moves, "Your next move:")]

    if move == "Stay":
        while python_score < 17:
            print(f"{python_name} hand is short. Taking additional card\n")
            sleep(2)
            card = get_card(cards_deck)
            python_score = calculate_score(card, python_score)
            python_cards.append(card)

    if not blackjack_winner:
        if python_score > 21:
            print_game_hands(python_cards, external_player_name, player_cards, player_score)
            print(f"Sorry {python_name}, it's a BUST")
            print(f"The winner is {external_player_name} !!!!\n")
            return external_player_name
        else:
            blackjack_winner = check_winner(player_score, python_score, external_player_name, player_cards, python_cards)
            print(f"The winner is {blackjack_winner} !!!!\n")
    return external_player_name


def blackjack():
    print("\nWelcome to Blackjack ♦ ♧ ♥ ♤")
    print("################################\n")
    print(the_rules + "\n")
    stop = False
    external_player_name = play_blackjack()
    while not stop:
        options = ["Yes", "No - Main Menu"]
        index = _single_selection(options, "Play again?")
        match index:
            case 0:
                play_blackjack(external_player_name)
            case 1:
                from main import start
                stop = True
                print("\nSee you later 🃏🃏🃏\n")
                start()


if __name__ == "__main__":
    blackjack()
