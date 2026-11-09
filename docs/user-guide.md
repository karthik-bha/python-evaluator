# Python Homework Evaluator: Handguide

This guide is for the mentor who configures assignments and reviews student
reports. The evaluator is a lightweight mentoring tool: it runs a submitted
Python file against configured input/output examples and records the result.

## How it behaves

- A push to the student repository triggers evaluation for changed Python files
  directly inside `assignments/<assignment-id>/submissions/`.
- The question ID is the filename segment before the first underscore. For
  example, `q1.py` and `q1_calculator.py` both select question `q1`.
- Each test case runs the same submission file in a fresh Python process with
  that case's `input_data` sent to standard input.
- Output is compared after trimming whitespace at the start and end. Internal
  spaces, line breaks, spelling, and capitalization must match.
- Every test case runs, even after an earlier test fails. The question score is
  the percentage of test cases that pass.
- The workflow creates one JSON report per changed file and one summary per
  assignment represented in the push. A summary covers only the submissions in
  that push; it is not a cumulative grade for every assignment question.

## Configure an assignment

In the evaluator repository, create this structure:

```text
assignments/
└── 01-python-basics/
    ├── assignment.json
    └── questions/
        ├── q1.json
        └── q2.json
```

`assignment.json` holds the display name and a shared time limit in seconds:

```json
{
  "name": "Python Basics",
  "time_limit_seconds": 2
}
```

Each question file has a name and at least one test case:

```json
{
  "name": "Add two numbers",
  "test_cases": [
    {
      "name": "positive values",
      "input_data": "5\n4\n",
      "expected_output": "9"
    },
    {
      "name": "zero values",
      "input_data": "0\n0\n",
      "expected_output": "0"
    }
  ]
}
```

The question ID is the JSON filename without `.json`; in this example it is
`q1`. Use IDs without underscores because the student workflow uses the first
underscore to separate an ID from an optional filename description. Keep
`input_data` and `expected_output` as JSON strings. Include `\n` where the
student program expects input lines or where expected output needs line breaks.

Every question currently inherits the assignment's time limit. There is no
per-question time limit setting yet.

## Student submission names

Students place files in the assignment's `submissions/` directory in the
training repository. Examples:

```text
assignments/01-python-basics/submissions/q1.py
assignments/01-python-basics/submissions/q2_strings.py
```

The assignment directory name must match the evaluator config directory, and
the question ID must match a file in that directory's `questions/` folder.
Each file is independently evaluated. If multiple files for the same question
are changed, each gets its own report.

## Run locally

From the root of the evaluator repository:

```powershell
python main.py --assignment 01-python-basics --question q1 `
  --submission ..\python-training\assignments\01-python-basics\submissions\q1_calculator.py
```

The report is printed to the terminal and written to
`evaluation_report.json`. Pass `--report-output <path>` to write it elsewhere.
The legacy format with `test_cases` directly in `assignment.json` can still be
run without `--question`.

## Read the verdicts and reports

| Verdict | Meaning |
| --- | --- |
| `AC` | The program exited successfully and its standard output matched. |
| `WA` | It exited successfully, but the output did not match. |
| `RE` | The process exited with an error. See `stderr` in the report. |
| `TLE` | The process exceeded the configured time limit. |
| `IE` | Reserved for internal errors; the current evaluator does not emit it. |

An individual report contains test totals, passed and failed counts, a
percentage score, and per-test expected output, actual output, exit code,
timeout flag, and captured standard error. The assignment summary combines the
test counts across successfully loaded question reports, and lists config
errors separately. It is weighted by test cases: a question with more test
cases contributes more to the overall percentage.

In GitHub Actions, download the `evaluation-reports` artifact from the workflow
run. It includes individual JSON reports and an `__summary.json` file per
assignment. The artifact retention period is 14 days.

## Things to watch out for

- **This is not a security sandbox.** A student program runs as a normal
  subprocess on the GitHub-hosted runner. A timeout does not limit memory,
  network access, filesystem access, or all child processes. Do not run code
  you consider hostile or sensitive on a runner with secrets or privileged
  access.
- **Standard output is the answer.** Debug messages printed to stdout can make
  an otherwise correct answer fail. Standard error is captured for diagnosis
  but is not compared against expected output.
- **Comparison is exact except for outer whitespace.** Numeric values are not
  parsed or rounded, and internal whitespace is significant.
- **The time limit applies per test case.** A question with many tests may take
  longer overall than one time limit interval.
- **Only changed submissions are evaluated.** Editing a question config alone
  does not trigger this workflow. Push a student file change to evaluate it.
- **A question config problem fails the workflow.** The workflow still creates
  an error report and attempts to upload reports, then marks the run failed.
  Check the Actions log for the underlying loader error.
- **The score reflects submitted questions only.** Missing submissions do not
  count as zero in the summary.
- **The evaluator checkout is not pinned to a release.** The workflow uses
  the evaluator repository's default branch at run time, so a later evaluator
  change can affect a training-repository run.

## Enhancement recommendations

1. **Isolate student execution before using less-trusted submissions.** Run
   each submission in a restricted container or separate disposable worker
   with CPU, memory, process, network, and filesystem limits.
2. **Pin the evaluator version.** Point the workflow at a tag or commit so a
   training run is reproducible and can be rolled back.
3. **Add per-question time limits and optional resource limits.** Some
   exercises may need different execution budgets.
4. **Add config schema/version validation.** Validate known fields and produce
   friendly errors before running any student program.
5. **Support cumulative assignment reports.** Store or collect prior reports
   when a true whole-assignment grade is needed; the current push summary is
   intentionally limited to files changed in that push.
6. **Improve feedback and report retention.** Include actionable config error
   details in artifacts and choose an artifact retention period that matches
   the mentoring workflow.

