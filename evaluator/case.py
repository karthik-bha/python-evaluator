from dataclasses import dataclass


@dataclass
class TestCase:
    __test__ = False

    name: str
    input_data: str
    expected_output: str