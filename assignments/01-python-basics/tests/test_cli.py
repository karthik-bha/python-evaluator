import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]


def test_question_cli_writes_identifiable_report(tmp_path):
    report_path = tmp_path / "q1-report.json"
    submission_path = (
        BASE_DIR
        / "assignments"
        / "01-python-basics"
        / "submissions"
        / "q1_calculator.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(BASE_DIR / "main.py"),
            "--assignment", "01-python-basics",
            "--question", "q1",
            "--submission", str(submission_path),
            "--report-output", str(report_path)
        ],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=True
    )

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["assignment_id"] == "01-python-basics"
    assert report["question_id"] == "q1"
    assert report["question"] == "Calculator"
    assert report["score"] == 100.0
    assert json.loads(result.stdout)["question_id"] == "q1"
