import argparse
import json
from pathlib import Path

from evaluator.reporter import generate_assignment_report


def main():
    parser = argparse.ArgumentParser(description="Aggregate question reports")
    parser.add_argument("--reports", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    reports = []
    for report_path in args.reports:
        with Path(report_path).open(encoding="utf-8") as file:
            reports.append(json.load(file))

    report = generate_assignment_report(reports)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=4), encoding="utf-8")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()
