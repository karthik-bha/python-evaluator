# Python Homework Evaluator

Evaluate student Python submissions against assignment test cases. Student
programs run as subprocesses with a configurable timeout; this is suitable for
mentoring workflows but is not a secure sandbox for hostile code.

## Assignment configuration

Assignment metadata and the shared execution time limit live in
`assignments/<assignment-id>/assignment.json`:

```json
{
  "name": "Python Basics",
  "time_limit_seconds": 2
}
```

Each question has an independent config at
`assignments/<assignment-id>/questions/<question-id>.json`:

```json
{
  "name": "Calculator",
  "test_cases": [
    {
      "name": "addition",
      "input_data": "5\n4\n+\n",
      "expected_output": "9.0"
    }
  ]
}
```

An optional non-negative integer `random_seed` on a test case runs that
submission with Python's random module seeded before the student's script
starts. Use it for repeatable tests of randomized exercises.

Question IDs are the config filename without `.json`. Student submission
filenames use that ID, optionally followed by an underscore and description:
`q1.py` and `q1_calculator.py` both map to question `q1`.

For compatibility, older assignments may still put `test_cases` in
`assignment.json` and be evaluated without `--question`.

## Run an evaluation

```powershell
python main.py --assignment 01-python-basics --question q1 `
  --submission assignments/01-python-basics/submissions/q1_calculator.py
```

The JSON report is printed and written to `evaluation_report.json`. Use
`--report-output <path>` to choose another report path. The Actions workflow
creates one report per changed submission and an assignment summary covering
the questions submitted in that push.

Run the tests with `python -m pytest`.

## Guides

- [User handguide](docs/user-guide.md): setup, intended behavior, reports,
  operational cautions, and recommended enhancements.
- [Architecture and core functions](docs/architecture.md): data flow,
  responsibilities of the main modules, workflow integration, and tests.
