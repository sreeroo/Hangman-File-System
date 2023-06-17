import pytest
from wrapper import *


class TestGetAttr:

    cases =pytest.mark.parametrize("file, content, size_var, result, size, nlink", [
        ('', '', None, 0, 0, 2), # root dir
        ('player', '', 'player_size', 0, 0, 1),
        ('player', 'HALLO WELT', 'player_size', 0, 10, 1),
        ('solution', '', 'solution_size', 0, 0, 1),
        ('solution', 'HALLO WELT', 'solution_size', 0, 10, 1),
        ('status', '', 'solution_size', 0, 0, 1),
        ('status', 'HALLO WELT', 'solution_size', 0, 10, 1),
        ('guesses', '', 'guesses_size', 0, 0, 1),
        ('guesses', 'HALLO WELT', 'guesses_size', 0, 10, 1),
        ('abc', '', None, -2, 0, None), # not existing file
    ])
    
    @cases
    def test_getattr(self, file, content, size_var, result, size, nlink):
        if size_var is not None:
            set_var(size_var, len(content))
        ret, stat = call_getattr('/' + file)
        assert ret == result
        assert stat.st_size == size
        if nlink is not None:
            assert stat.st_nlink == nlink
        assert is_guard_unchanged()
