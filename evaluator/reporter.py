
def generate_report(execution_results):
    total_tests = len(execution_results)

    passed = sum(
        1
        for result in execution_results
        if result["verdict"].value == "AC"
    )

    failed = total_tests - passed

    score = (
        round((passed / total_tests) * 100, 2)
        if total_tests > 0
        else 0.0
    )

    test_results = []

    for result in execution_results:
        test_case = result["test_case"]
        execution = result["execution"]
        verdict = result["verdict"]

        test_results.append({
            "name": test_case.name,
            "verdict": verdict.value,
            "expected_output": test_case.expected_output,
            "actual_output": execution["stdout"],
            "returncode": execution["returncode"],
            "timed_out": execution["timed_out"],
            "stderr": execution["stderr"]
        })

    return {
        "total_tests": total_tests,
        "passed": passed,
        "failed": failed,
        "score": score,
        "results": test_results
    }


def generate_assignment_report(question_reports):
    """Summarize the question reports present for this evaluation run."""
    questions = []
    total_tests = 0
    passed = 0
    errors = 0

    for report in question_reports:
        question = {
            "question_id": report.get("question_id"),
            "question": report.get("question"),
            "score": report.get("score", 0.0),
            "passed": report.get("passed", 0),
            "total_tests": report.get("total_tests", 0),
            "status": report.get("status", "evaluated")
        }
        questions.append(question)
        if question["status"] == "error":
            errors += 1
        total_tests += question["total_tests"]
        passed += question["passed"]

    return {
        "assignment_id": (question_reports[0].get("assignment_id")
                          if question_reports else None),
        "questions_submitted": len(questions),
        "questions_evaluated": len(questions) - errors,
        "question_errors": errors,
        "total_tests": total_tests,
        "passed": passed,
        "failed": total_tests - passed,
        "score": round((passed / total_tests) * 100, 2) if total_tests else 0.0,
        "questions": questions
    }
