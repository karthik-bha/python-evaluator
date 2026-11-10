from evaluator.runner import run_program


def test_run_program_supports_deterministic_random_seed(tmp_path):
    program = tmp_path / "random_value.py"
    (tmp_path / "helper.py").write_text("VALUE = 42\n", encoding="utf-8")
    program.write_text(
        "import random\nfrom helper import VALUE\n"
        "print(random.randint(1, 100) + VALUE - 42)\n",
        encoding="utf-8"
    )

    result = run_program(program, "", timeout=10, random_seed=7)

    assert result["returncode"] == 0
    assert result["stdout"].strip() == "42"
    assert not result["timed_out"]
