from pathlib import Path

from evaluator.config_loader import load_question_config
from evaluator.evaluator import evaluate_submission
from evaluator.verdicts import Verdict


ROOT_DIR = Path(__file__).resolve().parents[3]
ASSIGNMENTS_DIR = ROOT_DIR / "assignments"
ASSIGNMENT_ID = "02-python-homework"


def test_all_homework_question_configs_load():
    configs = [
        load_question_config(ASSIGNMENT_ID, f"q{number}", ASSIGNMENTS_DIR)
        for number in range(1, 6)
    ]

    assert [config.name for config in configs] == [
        "Multiplication Table",
        "Remove Duplicates from a List",
        "Student Grade Calculator",
        "Word Frequency Counter",
        "Number Guessing Game"
    ]
    assert all(config.test_cases for config in configs)


def test_number_guessing_tests_are_repeatable(tmp_path):
    submission = tmp_path / "guessing_game.py"
    submission.write_text(
        "import random\n"
        "target = random.randint(1, 100)\n"
        "attempts = 0\n"
        "while True:\n"
        "    guess = int(input())\n"
        "    attempts += 1\n"
        "    if guess < target:\n"
        "        print('Too low!')\n"
        "    elif guess > target:\n"
        "        print('Too high!')\n"
        "    else:\n"
        "        print(f'Correct! You guessed it in {attempts} attempts.')\n"
        "        break\n",
        encoding="utf-8"
    )
    config = load_question_config(ASSIGNMENT_ID, "q5", ASSIGNMENTS_DIR)

    results = evaluate_submission(
        submission,
        config.test_cases,
        timeout=10
    )

    assert all(result["verdict"] == Verdict.ACCEPTED for result in results)
