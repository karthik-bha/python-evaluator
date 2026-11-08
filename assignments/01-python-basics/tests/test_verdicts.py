from evaluator.verdicts import determine_verdict, Verdict

outputs = [
    {
        "returncode": 0,
        "stdout": "0\n",
        "stderr": "",
        "timed_out": True
    },
    {
        "returncode": 0,
        "stdout": "0\n",
        "stderr": "",
        "timed_out": False
    },
    {
        "returncode": None,
        "stdout": "0\n",
        "stderr": "",
        "timed_out": False
    }
    
]

def test_timeout_output():
    verdict= determine_verdict(outputs[0], True)

    assert verdict == Verdict.TIME_LIMIT_EXCEEDED

def test_correct_output():
    verdict= determine_verdict(outputs[1], True)
    
    assert verdict == Verdict.ACCEPTED

def test_incorrect_output():
    verdict= determine_verdict(outputs[1], False)
        
    assert verdict == Verdict.WRONG_ANSWER

def test_runtime_error():
    verdict= determine_verdict(outputs[2], False)
        
    assert verdict == Verdict.RUNTIME_ERROR