import pytest
from wrapper import *


class TestRead:

    cases =pytest.mark.parametrize("file, file_size, content, size, offset, expected_size", [
        # Read without offset
        ('player', 'player_size', 'WEINBERGSCHNECKE', 8, 0, None),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 8, 0, None),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 8, 0, None),
        # Read more than available
        ('player', 'player_size', 'WEINBERGSCHNECKE', 20, 0, None),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 20, 0, None),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 20, 0, None),
        # Read with offset
        ('player', 'player_size', 'WEINBERGSCHNECKE', 7, 4, None),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 7, 4, None),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 7, 4, None),
        # Read request that exceeds size of file is expected the be reduzed in size
        ('player', 'player_size', 'WEINBERGSCHNECKE', 8, 12, None),
        ('solution', 'solution_size', 'WEINBERGSCHNECKE', 8, 12, None),
        ('guesses', 'guesses_size', 'WEINBERGSCHNECKE', 8, 12, None),
        # Special cases
        ('', '', '', 0, 0, -2), # root dir
    ])
    
    @cases
    def test_read(self, file, file_size, content, size, offset, expected_size):
        buf_offset = 32
        if len(file):
            set_var(file, content)
        if len(file_size):
            set_var(file_size, len(content))
        buf_content = 20 * '12345678' # 160 characters
        buf = create_string_buffer(buf_content.encode('ascii'), size=len(buf_content))
        # Get a buffer object starting at an offset of the original buffer in the same memory location
        buf_with_offset = (c_byte * (len(buf_content) - buf_offset)).from_buffer(buf, buf_offset)
        # Do with strings what the read will do in the buffer
        if expected_size is None: # automatic calculation
            expected_size = size
            if offset + size > len(content):
                expected_size = len(content) - offset
        ret_expected_size = expected_size
        if expected_size < 0:
            expected_size = 0            
        value_expected = buf_content[0:buf_offset] + content[offset:offset+expected_size] + buf_content[buf_offset+expected_size:]
        # Call the read function
        ret_size = call_read('/' + file, buf_with_offset, size, offset)
        buf_content_new = bytearray(buf).decode('ascii')
        #print(buf_content_new)
        #print(value_expected)
        # Check results
        if ret_expected_size < 0:
            assert ret_size < 0
        else:
            assert ret_size == ret_expected_size
        # Check correctness of new buffer content
        assert content[offset:offset+expected_size] == buf_content_new[buf_offset:buf_offset+expected_size]
        assert buf_content[0:buf_offset] == buf_content_new[0:buf_offset]
        assert buf_content[buf_offset+expected_size:] == buf_content_new[buf_offset+expected_size:]
        # This is redundant and checks in a single comparison
        assert bytearray(buf).decode('ascii') == value_expected
        # Final guard check
        assert is_guard_unchanged()
