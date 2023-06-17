import pytest
from wrapper import *


class TestImmediatePlaying:

    def test_playing_weinbergschnecke(self):
        assert read_file('/solution') == 'WEINBERGSCHNECKE'
        assert read_file('/guesses') == ''
        assert read_file('/status') == '----------------'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'N')
        assert is_guard_unchanged()        
        assert read_file('/status') == '---N-------N----'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'G')
        assert is_guard_unchanged()        
        assert read_file('/status') == '---N---G---N----'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'S')
        assert is_guard_unchanged()        
        assert read_file('/status') == '---N---GS--N----'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'H')
        assert is_guard_unchanged()        
        assert read_file('/status') == '---N---GS-HN----'
        assert is_guard_unchanged()
