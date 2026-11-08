from evaluator.runner import run_program
from evaluator.comparator import compare_output
from evaluator.verdicts import determine_verdict


def evaluate_submission(file_path, test_cases,  timeout: float = 2.0):
    execution_results = []

    for test_case in test_cases:
        output = run_program(
            file_path,
            test_case.input_data,
            timeout=timeout
        )

        is_correct = (
            output["returncode"] == 0
            and not output["timed_out"]
            and compare_output(
                output["stdout"],
                test_case.expected_output
            )
        )

        verdict = determine_verdict(output, is_correct)

        execution_results.append({
            "test_case": test_case,
            "execution": output,
            "verdict": verdict
        })

    return execution_results
