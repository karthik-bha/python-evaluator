import json

import pytest

from evaluator.config_loader import load_assignment_config, load_question_config


def test_load_assignment_config(tmp_path):
    assignment_dir = tmp_path / "01-python-basics"
    assignment_dir.mkdir()

    config_data = {
        "name": "Calculator",
        "time_limit_seconds": 2,
        "test_cases": [
            {
                "name": "addition",
                "input_data": "5\n4\n+\n",
                "expected_output": "9.0"
            }
        ]
    }

    config_file = assignment_dir / "assignment.json"

    config_file.write_text(
        json.dumps(config_data),
        encoding="utf-8"
    )

    config = load_assignment_config(
        "01-python-basics",
        tmp_path
    )

    assert config.name == "Calculator"
    assert config.time_limit_seconds == 2
    assert len(config.test_cases) == 1
    assert config.test_cases[0].name == "addition"


def test_missing_assignment():
    with pytest.raises(FileNotFoundError):
        load_assignment_config("missing", "assignments")


def test_invalid_assignment_id(tmp_path):
    with pytest.raises(ValueError):
        load_assignment_config("../outside", tmp_path)


def test_load_question_config(tmp_path):
    assignment_dir = tmp_path / "basics"
    questions_dir = assignment_dir / "questions"
    questions_dir.mkdir(parents=True)
    (assignment_dir / "assignment.json").write_text(
        json.dumps({"name": "Basics", "time_limit_seconds": 1.5}),
        encoding="utf-8"
    )
    (questions_dir / "q1.json").write_text(json.dumps({
        "name": "Calculator",
        "test_cases": [{
            "name": "addition",
            "input_data": "1\n2\n+\n",
            "expected_output": "3"
        }]
    }), encoding="utf-8")

    config = load_question_config("basics", "q1", tmp_path)

    assert config.question_id == "q1"
    assert config.name == "Calculator"
    assert config.time_limit_seconds == 1.5
    assert config.test_cases[0].name == "addition"


def test_missing_question_config(tmp_path):
    assignment_dir = tmp_path / "basics"
    assignment_dir.mkdir()
    (assignment_dir / "assignment.json").write_text(
        json.dumps({"name": "Basics"}), encoding="utf-8"
    )

    with pytest.raises(FileNotFoundError, match="Question configuration"):
        load_question_config("basics", "q1", tmp_path)


def test_invalid_question_id(tmp_path):
    with pytest.raises(ValueError, match="question ID"):
        load_question_config("basics", "../outside", tmp_path)
