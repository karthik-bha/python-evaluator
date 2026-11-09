from pathlib import Path

from evaluator.config_loader import load_question_config
from evaluator.evaluator import evaluate_submission
from evaluator.verdicts import Verdict


BASE_DIR = Path(__file__).resolve().parents[3]

ASSIGNMENTS_DIR = BASE_DIR / "assignments"

config = load_question_config("01-python-basics", "q1", ASSIGNMENTS_DIR)

STUDENT_FILE = (
    ASSIGNMENTS_DIR
    / "01-python-basics"
    / "submissions"
    / "q1_calculator.py"
)


def test_evaluator():
    output = evaluate_submission(
        STUDENT_FILE,
        config.test_cases,
        timeout=config.time_limit_seconds
    )

    assert len(output) == 3
    assert all(result["verdict"] == Verdict.ACCEPTED for result in output)
