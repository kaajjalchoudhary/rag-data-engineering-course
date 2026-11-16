import importlib
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TARGET = os.environ.get("COURSE_TARGET", "solutions")


@pytest.fixture
def mod(request):
    """Load the module under test from solutions/ or exercises/ (COURSE_TARGET)."""
    name = request.node.get_closest_marker("module").args[0]
    return importlib.import_module(f"{TARGET}.{name}")


def pytest_configure(config):
    config.addinivalue_line("markers", "module(name): course module the test checks")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    outcome = yield
    if outcome.excinfo and issubclass(outcome.excinfo[0], NotImplementedError):
        outcome.force_exception(pytest.skip.Exception(f"{item.name}: not attempted yet"))
