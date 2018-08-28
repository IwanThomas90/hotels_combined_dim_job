import os
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def sample_fixture() -> str:
    return "hello"
