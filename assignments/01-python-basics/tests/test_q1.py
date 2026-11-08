from pathlib import Path
from evaluator.runner import run_program
from evaluator.evaluator import evaluate_submission


BASE_DIR = Path(__file__).resolve().parents[3]

ASSIGNMENT_DIR = BASE_DIR / "assignments" / "01-python-basics"

STUDENT_FILE = (
    ASSIGNMENT_DIR / "submissions" / "q1_calculator.py"
)

FIXTURES_DIR = ASSIGNMENT_DIR / "tests" / "fixtures"

RUNTIME_ERROR_FILE = FIXTURES_DIR / "runtime_error.py"
WRONG_ANSWER_FILE = FIXTURES_DIR / "wrong_answer.py"
INFINITE_LOOP_FILE = FIXTURES_DIR / "infinite_loop.py"

def test_calculator_addition():
    input_data = "5\n4\n+\n"
    output = run_program(STUDENT_FILE, input_data)

    assert output["returncode"] == 0, output["stderr"]
    assert output["stdout"].strip() == "9.0"


def test_runtime_error():
    output = run_program(RUNTIME_ERROR_FILE, "invalid input")

    assert output["returncode"] != 0
    assert output["stderr"] != ""
    assert not output["timed_out"]


def test_wrong_answer():
    input_data = "5\n4\n+\n"
    output = run_program(WRONG_ANSWER_FILE, input_data)

    assert output["returncode"] == 0
    assert output["stdout"].strip() != "9.0"


def test_timeout():
    output = run_program(INFINITE_LOOP_FILE, "")

    assert output["timed_out"] is True
