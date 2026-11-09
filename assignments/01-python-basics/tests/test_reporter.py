from evaluator.reporter import generate_assignment_report, generate_report
from evaluator.verdicts import Verdict
from evaluator.case import TestCase


def make_result(name, verdict):
    return {
        "test_case": TestCase(
            name=name,
            input_data="",
            expected_output="expected"
        ),
        "execution": {
            "returncode": 0,
            "stdout": "actual",
            "stderr": "",
            "timed_out": False
        },
        "verdict": verdict
    }


def test_report_scoring():
    results = [
        make_result("addition", Verdict.ACCEPTED),
        make_result("subtraction", Verdict.ACCEPTED),
        make_result("multiplication", Verdict.WRONG_ANSWER)
    ]

    report = generate_report(results)

    assert report["total_tests"] == 3
    assert report["passed"] == 2
    assert report["failed"] == 1
    assert report["score"] == 66.67


def test_empty_report():
    report = generate_report([])

    assert report["total_tests"] == 0
    assert report["passed"] == 0
    assert report["failed"] == 0
    assert report["score"] == 0.0


def test_report_contains_verdicts():
    results = [
        make_result("addition", Verdict.ACCEPTED),
        make_result("subtraction", Verdict.RUNTIME_ERROR)
    ]

    report = generate_report(results)

    assert report["results"][0]["verdict"] == "AC"
    assert report["results"][1]["verdict"] == "RE"


def test_assignment_report_aggregates_submitted_questions():
    report = generate_assignment_report([
        {
            "assignment_id": "basics",
            "question_id": "q1",
            "question": "Calculator",
            "passed": 2,
            "total_tests": 2,
            "score": 100.0
        },
        {
            "assignment_id": "basics",
            "question_id": "q2",
            "question": "Strings",
            "passed": 1,
            "total_tests": 2,
            "score": 50.0
        }
    ])

    assert report["assignment_id"] == "basics"
    assert report["questions_submitted"] == 2
    assert report["questions_evaluated"] == 2
    assert report["total_tests"] == 4
    assert report["passed"] == 3
    assert report["score"] == 75.0
