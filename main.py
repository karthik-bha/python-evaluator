import argparse
import json
from pathlib import Path

from evaluator.config_loader import load_assignment_config, load_question_config
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
    parser.add_argument("--question", help="Question ID, such as q1")
    parser.add_argument("--report-output", help="Optional report output path")

    args = parser.parse_args()

    assignment = load_assignment_config(args.assignment, ASSIGNMENTS_DIR)
    if args.question:
        config = load_question_config(
            args.assignment, args.question, ASSIGNMENTS_DIR
        )
    else:
        config = assignment
        if not config.test_cases:
            parser.error("--question is required for question-based assignments")

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
    report["assignment"] = assignment.name
    report["assignment_id"] = args.assignment
    if args.question:
        report["question"] = config.name
        report["question_id"] = args.question

    report_json = json.dumps(report, indent=4)

    print(report_json)

    report_path = (
        Path(args.report_output).resolve()
        if args.report_output
        else ROOT_DIR / "evaluation_report.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", encoding="utf-8") as file:
        file.write(report_json)


if __name__ == "__main__":
    main()
