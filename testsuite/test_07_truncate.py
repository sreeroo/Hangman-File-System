import pytest
from wrapper import *


class TestTruncate:

    cases =pytest.mark.parametrize("file, file_size, content, offset, expected_result, expected_file_size", [
        # Truncate to zero
        ('player', 'player_size', 'WEINBERGSCHNECKE', 0, 0, 0),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 0, 0, 0),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 0, 0, 0),
        # Truncate to 8
        ('player', 'player_size', 'WEINBERGSCHNECKE', 8, 0, 8),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 8, 0, 8),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 8, 0, 8),
        # Truncate to 32
        ('player', 'player_size', 'WEINBERGSCHNECKE', 24, 0, 24),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 24, 0, 24),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 24, 0, 24),
    ])
    
    @cases
    def test_truncate(self, file, file_size, content, offset, expected_result, expected_file_size):
        # Fill 32 bytes of file memory with defined content pattern
        set_var(file, 32 * '#')
        # Set file data
        if len(file):
            set_var(file, content)
        if len(file_size):
            set_var(file_size, len(content))
        # Call the truncate function
        ret = call_truncate('/' + file, offset)
        # Check results
        vars = get_vars()
        assert ret == expected_result
        assert vars[file_size] == expected_file_size
        # Check new file content
        file_content = bytearray(get_var(file)).decode('ascii')[0:expected_file_size]
        num_zeroes = 0 if (offset < len(content)) else (offset - len(content))
        file_content_expected = content[0:offset] + num_zeroes * '\0'
        assert file_content == file_content_expected
        # Final guard check
        assert is_guard_unchanged()
