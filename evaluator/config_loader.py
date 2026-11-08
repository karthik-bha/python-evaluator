import json
from dataclasses import dataclass
from pathlib import Path

from evaluator.case import TestCase


@dataclass
class AssignmentConfig:
    name: str
    time_limit_seconds: float
    test_cases: list[TestCase]


def load_assignment_config(assignment_id, assignments_root):
    root = Path(assignments_root).resolve()

    if not assignment_id or Path(assignment_id).name != assignment_id:
        raise ValueError("Invalid assignment ID")

    assignment_dir = (root / assignment_id).resolve()

    if root not in assignment_dir.parents:
        raise ValueError("Invalid assignment path")

    config_path = assignment_dir / "assignment.json"

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Assignment configuration not found: {config_path}"
        )

    with config_path.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Assignment configuration must be a JSON object")

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

    if not isinstance(raw_test_cases, list) or not raw_test_cases:
        raise ValueError("At least one test case is required")

    test_cases = []

    for index, case in enumerate(raw_test_cases):
        if not isinstance(case, dict):
            raise ValueError(f"Invalid test case at index {index}")

        for field in ("name", "input_data", "expected_output"):
            if not isinstance(case.get(field), str):
                raise ValueError(
                    f"Test case {index}: '{field}' must be a string"
                )

        test_cases.append(
            TestCase(
                name=case["name"],
                input_data=case["input_data"],
                expected_output=case["expected_output"]
            )
        )

    return AssignmentConfig(
        name=name,
        time_limit_seconds=float(timeout),
        test_cases=test_cases
    )
