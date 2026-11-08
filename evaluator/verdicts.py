from enum import Enum 

class Verdict(Enum):
    ACCEPTED = "AC"
    WRONG_ANSWER = "WA"
    RUNTIME_ERROR = "RE"
    TIME_LIMIT_EXCEEDED = "TLE"
    INTERNAL_ERROR = "IE"

def determine_verdict(output, is_correct):
    if output["timed_out"]:
        return Verdict.TIME_LIMIT_EXCEEDED

    if output["returncode"] is None or output["returncode"] != 0:
        return Verdict.RUNTIME_ERROR

    if is_correct:
        return Verdict.ACCEPTED

    return Verdict.WRONG_ANSWER