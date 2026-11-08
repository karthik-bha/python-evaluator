import subprocess
from pathlib import Path
import sys

# BASE_DIR= Path(__file__).resolve().parent.parent

# file_path= BASE_DIR/"assignments" # to be replaced with vars
# input_data="4\n5\n+\n"


def run_program(file_path, input_data, timeout: float = 2.0):
    """
    Execute a Python file with the provided input.

    Return:
        returncode
        stdout
        stderr
    """
    final_payload={
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "timed_out": True
    }
    try:
        result= subprocess.run(
            [sys.executable, str(file_path)], #sys.executable instead of explicit python3.x so that it uses the interpreter's version
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        final_payload={
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False
        }
        return final_payload
    except subprocess.TimeoutExpired as exc:
        final_payload["stderr"] = exc.stderr or ""
        final_payload["stdout"] = exc.stdout or ""
        return final_payload


# output= run_program(file_path=file_path, input_data=input_data)
# print(output)
