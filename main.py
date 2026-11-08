import argparse
import json
from pathlib import Path

from evaluator.config_loader import load_assignment_config
from evaluator.evaluator import evaluate_submission
from evaluator.reporter import generate_report


ROOT_DIR = Path(__file__).resolve().parent
ASSIGNMENTS_DIR = ROOT_DIR / "assignments"


def main():
    parser = argparse.ArgumentParser(
        description="Python Homework Evaluator"
    )

    parser.add_argument(
        "--assignment",
        required=True,
        help="Assignment folder name"
    )

    parser.add_argument(
        "--submission",
        required=True,
        help="Path to the student's Python submission"
    )

    args = parser.parse_args()

    config = load_assignment_config(
        args.assignment,
        ASSIGNMENTS_DIR
    )

    submission_path = Path(args.submission)

    if not submission_path.is_absolute():
        submission_path = ROOT_DIR / submission_path

    if not submission_path.is_file():
        raise FileNotFoundError(
            f"Submission not found: {submission_path}"
        )

    results = evaluate_submission(
        submission_path,
        config.test_cases,
        timeout=config.time_limit_seconds
    )

    report = generate_report(results)
    report["assignment"] = config.name

    report_json = json.dumps(report, indent=4)

    print(report_json)

    report_path = ROOT_DIR / "evaluation_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        file.write(report_json)


if __name__ == "__main__":
    main()
