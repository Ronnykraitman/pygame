import random
import sys
import time
from time import sleep
import concurrent.futures
import requests
from common.colors import Bright_Cyan, Color_Off
from common.logos import progress_bar
from simple_term_menu import TerminalMenu
import html

from utils.functions import get_user_name, _single_selection


def _get_all_categories() -> dict:
    categories_and_ids: dict = {}
    url = "https://opentdb.com/api_category.php"
    headers = {"Content-Type": "application/json", "accept": "*/*"}
    data = {
        "method": "get",
        "postParams": {},
        "urlParams": {}
    }
    response = requests.post(url, headers=headers, json=data)
    response_as_dict: dict = response.json()
    response_as_list: list = response_as_dict.get("trivia_categories")

    categories_and_ids.update({"Any Category": "0"})
    for category_and_id in response_as_list:
        category_id = category_and_id["id"]
        category_name = category_and_id["name"]
        categories_and_ids.update({category_name: category_id})

    return categories_and_ids


def _select_categories() -> tuple:
    categories_and_ids: dict = _get_all_categories()
    categories = categories_and_ids.keys()
    terminal_menu = TerminalMenu(
        categories,
        title="Available Categories",
        multi_select=True,
        show_multi_select_hint=True,
    )
    terminal_menu.show()
    return list(terminal_menu.chosen_menu_entries), categories_and_ids


def _select_difficulty():
    difficulty_options = ["Easy", "Medium", "Hard"]
    terminal_menu = TerminalMenu(
        difficulty_options, title="Difficulty Level")
    index = terminal_menu.show()
    return difficulty_options[index]


def _build_url(difficulty, category, category_to_id):
    if category == "0":
        return f"https://opentdb.com/api.php?amount=10&difficulty={difficulty}&type=boolean"

    category_id = category_to_id.get(category)
    return f"https://opentdb.com/api.php?amount=5&category={category_id}&difficulty={difficulty}&type=boolean"


def _handle_request(url):
    headers = {"Content-Type": "application/json", "accept": "*/*"}
    data = {
        "method": "get",
        "postParams": {},
        "urlParams": {}
    }
    number_of_attempts = 0
    response_code = 9
    response_as_dict: dict = {}
    while response_code != 0 and number_of_attempts < 3:
        response_as_dict = requests.post(url, headers=headers, json=data).json()
        response_code = response_as_dict.get("response_code")
        if response_code == 1:
            return {}
        number_of_attempts += 1
        sleep(5)  # API can get 1 request each 5 second per IP address
    return response_as_dict.get("results")


def _get_questions_from_url(difficulty, category, category_to_id) -> dict:
    questions_and_answers: dict = {}
    url = _build_url(difficulty, category, category_to_id)
    results: list = _handle_request(url)
    for result in results:
        questions_and_answers.update(
            {result["question"]: {"correct_answer": result["correct_answer"], "category": result["category"]}})
    return questions_and_answers


def print_progress_bar():
    print("Fetching the best possible questions for you. Hang tight..\n")
    for i in range(len(progress_bar)):
        time.sleep(0.5)
        sys.stdout.write("\r" + progress_bar[i % len(progress_bar)])
        sys.stdout.flush()
    print()


def send_request(categories: list, category_to_id: dict, difficulty: str) -> dict:
    if categories.__contains__("Any Category"):
        return _get_questions_from_url(difficulty, "0", category_to_id)
    else:
        questions_and_answers: dict = {}
        for category in categories:
            questions_and_answers.update(_get_questions_from_url(difficulty, category, category_to_id))
        return questions_and_answers


def get_questions():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        difficulty = _select_difficulty().lower()
        selected_categories, category_to_id = _select_categories()
        future1 = executor.submit(print_progress_bar)
        future2 = executor.submit(send_request, selected_categories, category_to_id, difficulty)
        concurrent.futures.wait([future1, future2])
    return future2.result()


def arrange_questions(questions_and_answers_dict: dict):
    questions_and_answers_as_list: list = []
    for question in questions_and_answers_dict.items():
        questions_and_answers_as_list.append(question)
    return questions_and_answers_as_list


def play_brain_quiz(external_player_name=None):
    questions_and_answers_as_list: list = []
    already_asked_questions_indexes = []

    if external_player_name is None:
        external_player_name = f"{Bright_Cyan}{get_user_name()}{Color_Off}"

    while not questions_and_answers_as_list:
        questions_and_answers: dict = get_questions()
        questions_and_answers_as_list = arrange_questions(questions_and_answers)
        if not questions_and_answers_as_list:
            print("No good questions for the selected categories. Please select different ones\n")

    next_question_request = True
    while next_question_request and len(already_asked_questions_indexes) < len(questions_and_answers_as_list):
        random_index = random.randint(0, len(questions_and_answers_as_list) - 1)
        while random_index in already_asked_questions_indexes:
            random_index = random.randint(0, len(questions_and_answers_as_list) - 1)

        already_asked_questions_indexes.append(random_index)

        question_html = (questions_and_answers_as_list[random_index][0]).replace(".", "") + "?"
        question = html.unescape(question_html)
        category = html.unescape(questions_and_answers_as_list[random_index][1].get("category"))
        correct_answer = questions_and_answers_as_list[random_index][1].get("correct_answer")

        print(f"\nOK {external_player_name}, Here is a {category} question:")
        print(question + "\n")

        answer_options = ["True", "False"]
        index = _single_selection(answer_options, title="True Or False?")
        user_answer = answer_options[index]

        if user_answer == correct_answer:
            print("You are right!!!\n")
        else:
            print("You got it wrong. Try the next time\n")

        next_options = ["Yes", "No"]
        index = _single_selection(next_options, title="Another question?")
        next_question_request = True if next_options[index] == "Yes" else False
        if len(already_asked_questions_indexes) == len(questions_and_answers_as_list):
            print("No more questions to ask :(\n")

    print("Game Over\n")
    return external_player_name


def brain_quiz():
    stop = False
    user_name = play_brain_quiz()
    while not stop:
        options = ["Yes", "No - Main Menu"]
        index = _single_selection(options, "Play again?")
        match index:
            case 0:
                play_brain_quiz(user_name)
            case 1:
                from main import start
                stop = True
                print("\nSee you later 👾👾👾\n")
                start()
