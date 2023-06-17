import pytest
from wrapper import *


class TestPlaying:

    def test_playing_weinbergschnecke(self):
        assert call_truncate('/solution', 0) == 0
        assert is_guard_unchanged()        
        assert write_file('/solution', 'WEINBERGSCHNECKE')
        assert is_guard_unchanged()        
        assert read_file('/solution') == 'WEINBERGSCHNECKE'
        assert is_guard_unchanged()        
        assert call_truncate('/guesses', 0) == 0
        assert is_guard_unchanged()        
        assert read_file('/guesses') == ''
        assert is_guard_unchanged()
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

    def test_playing_sonne(self):
        assert call_truncate('/solution', 0) == 0
        assert is_guard_unchanged()        
        assert write_file('/solution', 'SONNE')
        assert is_guard_unchanged()        
        assert read_file('/solution') == 'SONNE'
        assert is_guard_unchanged()        
        assert call_truncate('/guesses', 0) == 0
        assert is_guard_unchanged()        
        assert read_file('/guesses') == ''
        assert is_guard_unchanged()
        assert read_file('/status') == '-----'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'N')
        assert is_guard_unchanged()        
        assert read_file('/status') == '--NN-'
        assert is_guard_unchanged()
        assert append_file('/guesses', 'S')
        assert is_guard_unchanged()        
        assert read_file('/status') == 'S-NN-'
        assert is_guard_unchanged()
