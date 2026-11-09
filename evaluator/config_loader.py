import json
from dataclasses import dataclass
from pathlib import Path

from evaluator.case import TestCase


@dataclass
class AssignmentConfig:
    name: str
    time_limit_seconds: float
    test_cases: list[TestCase]


@dataclass
class QuestionConfig:
    question_id: str
    name: str
    time_limit_seconds: float
    test_cases: list[TestCase]


def _parse_test_cases(raw_test_cases, label):
    if not isinstance(raw_test_cases, list) or not raw_test_cases:
        raise ValueError(f"At least one test case is required in {label}")

    test_cases = []
    for index, case in enumerate(raw_test_cases):
        if not isinstance(case, dict):
            raise ValueError(f"Invalid test case at index {index} in {label}")

        for field in ("name", "input_data", "expected_output"):
            if not isinstance(case.get(field), str):
                raise ValueError(
                    f"Test case {index} in {label}: '{field}' must be a string"
                )

        test_cases.append(TestCase(
            name=case["name"],
            input_data=case["input_data"],
            expected_output=case["expected_output"]
        ))
    return test_cases


def _load_json_object(config_path, label):
    if not config_path.is_file():
        raise FileNotFoundError(f"{label} configuration not found: {config_path}")
    with config_path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{label} configuration must be a JSON object")
    return data


def _validate_id(value, label):
    if (not isinstance(value, str) or not value
            or Path(value).name != value or value in (".", "..")):
        raise ValueError(f"Invalid {label} ID")


def load_assignment_config(assignment_id, assignments_root):
    root = Path(assignments_root).resolve()

    _validate_id(assignment_id, "assignment")

    assignment_dir = (root / assignment_id).resolve()

    if root not in assignment_dir.parents:
        raise ValueError("Invalid assignment path")

    config_path = assignment_dir / "assignment.json"

    data = _load_json_object(config_path, "Assignment")

    name = data.get("name")
    timeout = data.get("time_limit_seconds", 2)
    raw_test_cases = data.get("test_cases")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Assignment name is required")

    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError("Time limit must be a positive number")

    test_cases = _parse_test_cases(raw_test_cases, "assignment.json") if raw_test_cases is not None else []

    return AssignmentConfig(
        name=name,
        time_limit_seconds=float(timeout),
        test_cases=test_cases
    )


def load_question_config(assignment_id, question_id, assignments_root):
    _validate_id(assignment_id, "assignment")
    _validate_id(question_id, "question")
    assignment = load_assignment_config(assignment_id, assignments_root)
    assignment_dir = (Path(assignments_root).resolve() / assignment_id).resolve()
    questions_dir = (assignment_dir / "questions").resolve()
    if assignment_dir not in questions_dir.parents:
        raise ValueError("Invalid questions path")

    data = _load_json_object(questions_dir / f"{question_id}.json", "Question")
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Question name is required")

    return QuestionConfig(
        question_id=question_id,
        name=name,
        time_limit_seconds=assignment.time_limit_seconds,
        test_cases=_parse_test_cases(data.get("test_cases"), f"question {question_id}")
    )
