import pytest
from wrapper import *


class TestReadDir:

    @pytest.fixture()
    def root_dir(self):
        ret, files = call_readdir('/')
        yield ret, files

    def test_readdir_root_contains_current(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert '.' in files
        assert is_guard_unchanged()

    def test_readdir_root_contains_parent(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert '..' in files
        assert is_guard_unchanged()

    def test_readdir_root_contains_player(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert 'player' in files
        assert is_guard_unchanged()

    def test_readdir_root_contains_solution(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert 'solution' in files
        assert is_guard_unchanged()

    def test_readdir_root_contains_status(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert 'status' in files
        assert is_guard_unchanged()

    def test_readdir_root_contains_guesses(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert 'guesses' in files
        assert is_guard_unchanged()

    def test_readdir_root_num_files_correct(self, root_dir):
        ret, files = root_dir
        assert ret == 0
        assert len(files) == 6
        assert is_guard_unchanged()

    def test_readdir_other_directory_should_fail(self):
        ret, files = call_readdir('/abc')
        assert ret != 0
        assert len(files) == 0
        assert is_guard_unchanged()
