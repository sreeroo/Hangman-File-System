import pytest
from wrapper import *


class TestImplementedFunctions:

    @pytest.fixture()
    def fuse_operations(self):
        fuse_ops = fuse_operations_alt.in_dll(ccode, 'fs_operations')
        yield fuse_ops

    def test_fs_readdir(self):
        """Check if fs_readdir is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_readdir'))
        assert fct_addr is not None

    def test_fs_getattr(self):
        """Check if fs_getattr is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_getattr'))
        assert fct_addr is not None

    def test_fs_readdir(self):
        """Check if fs_readdir is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_readdir'))
        assert fct_addr is not None

    def test_fs_open(self):
        """Check if fs_open is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_open'))
        assert fct_addr is not None

    def test_fs_read(self):
        """Check if fs_read is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_read'))
        assert fct_addr is not None

    def test_fs_write(self):
        """Check if fs_write is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_write'))
        assert fct_addr is not None

    def test_fs_truncate(self):
        """Check if fs_truncate is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_truncate'))
        assert fct_addr is not None

    def test_fs_readdir_called(self, fuse_operations):
        """Check if fs_readdir is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_readdir'))
        assert fct_addr == fuse_operations.readdir

    def test_fs_getattr_called(self, fuse_operations):
        """Check if fs_getattr is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_getattr'))
        assert fct_addr == fuse_operations.getattr

    def test_fs_readdir_called(self, fuse_operations):
        """Check if fs_readdir is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_readdir'))
        assert fct_addr == fuse_operations.readdir

    def test_fs_open_called(self, fuse_operations):
        """Check if fs_open is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_open'))
        assert fct_addr == fuse_operations.open

    def test_fs_read_called(self, fuse_operations):
        """Check if fs_read is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_read'))
        assert fct_addr == fuse_operations.read

    def test_fs_write_called(self, fuse_operations):
        """Check if fs_write is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_write'))
        assert fct_addr == fuse_operations.write

    def test_fs_truncate_called(self, fuse_operations):
        """Check if fs_truncate is implemented and being called"""
        fct_addr = addressof(c_void_p.in_dll(ccode, 'fs_truncate'))
        assert fct_addr == fuse_operations.truncate

    def test_unlink(self, fuse_operations):
        """Check if fs_unlink is not implemented/called"""
        assert fuse_operations.unlink is None

    def test_flush(self, fuse_operations):
        """Check if fs_flush is not implemented/called"""
        assert fuse_operations.flush is None
