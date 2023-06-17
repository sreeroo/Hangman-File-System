import pytest
from wrapper import *


O_RDONLY = 0x0000
O_WRONLY = 0x0001
O_TRUNC = 0x0200


class TestOpen:

    cases =pytest.mark.parametrize("file, file_size, content, flags, expected_result, expected_file_size", [
        # Open for read
        ('player', 'player_size', 'WEINBERGSCHNECKE', O_RDONLY, 0, 16),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', O_RDONLY, 0, 16),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', O_RDONLY, 0, 16),
        # Open for write
        ('player', 'player_size', 'WEINBERGSCHNECKE', O_WRONLY, 0, 16),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', O_WRONLY, 0, 16),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', O_WRONLY, 0, 16),
        # Truncate to size zero
        ('player', 'player_size', 'WEINBERGSCHNECKE', O_WRONLY | O_TRUNC, 0, 0),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', O_WRONLY | O_TRUNC, 0, 0),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', O_WRONLY | O_TRUNC, 0, 0),
    ])
    
    @cases
    def test_open(self, file, file_size, content, flags, expected_result, expected_file_size):
        if len(file):
            set_var(file, content)
        if len(file_size):
            set_var(file_size, len(content))
        # Call the open function
        ret = call_open('/' + file, flags)
        # Check results
        vars = get_vars()
        assert ret == expected_result
        assert vars[file_size] == expected_file_size
        # Final guard check
        assert is_guard_unchanged()
