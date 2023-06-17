import pytest
from wrapper import *


class TestUnchangedStructure:

    def test_variables(self):
        """Check whether variables can be read"""
        get_vars()

    def test_guard_unchanged(self):
        """Check whether the guard variables are set correctly"""
        get_vars()
        assert is_guard_unchanged()
