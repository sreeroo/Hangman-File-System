from ctypes import *
from platform import machine, system

# Load the shared object file
ccode = CDLL('./hangman_fs.so')


# Type definition from https://github.com/FiloSottile/camlistore/blob/master/lib/python/fusepy/fuse3.py
# Corrections based on http://libfuse.github.io/doxygen/structfuse__operations.html

class c_timespec(Structure):
    _fields_ = [('tv_sec', c_long), ('tv_nsec', c_long)]

class c_utimbuf(Structure):
    _fields_ = [('actime', c_timespec), ('modtime', c_timespec)]

class c_stat(Structure):
    pass    # Platform dependent

_system = system()
if _system in ('Darwin', 'FreeBSD'):
    _libiconv = CDLL(find_library("iconv"), RTLD_GLOBAL)     # libfuse dependency
    ENOTSUP = 45
    c_dev_t = c_int32
    c_fsblkcnt_t = c_ulong
    c_fsfilcnt_t = c_ulong
    c_gid_t = c_uint32
    c_mode_t = c_uint16
    c_off_t = c_int64
    c_pid_t = c_int32
    c_uid_t = c_uint32
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte),
        c_size_t, c_int, c_uint32)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte),
        c_size_t, c_uint32)
    c_stat._fields_ = [
        ('st_dev', c_dev_t),
        ('st_ino', c_uint32),
        ('st_mode', c_mode_t),
        ('st_nlink', c_uint16),
        ('st_uid', c_uid_t),
        ('st_gid', c_gid_t),
        ('st_rdev', c_dev_t),
        ('st_atimespec', c_timespec),
        ('st_mtimespec', c_timespec),
        ('st_ctimespec', c_timespec),
        ('st_size', c_off_t),
        ('st_blocks', c_int64),
        ('st_blksize', c_int32)]
elif _system == 'Linux':
    ENOTSUP = 95
    c_dev_t = c_ulonglong
    c_fsblkcnt_t = c_ulonglong
    c_fsfilcnt_t = c_ulonglong
    c_gid_t = c_uint
    c_mode_t = c_uint
    c_off_t = c_longlong
    c_pid_t = c_int
    c_uid_t = c_uint
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t, c_int)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t)

    _machine = machine()
    if _machine == 'x86_64':
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('st_ino', c_ulong),
            ('st_nlink', c_ulong),
            ('st_mode', c_mode_t),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('__pad0', c_int),
            ('st_rdev', c_dev_t),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_long),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_reserved1', c_long),            
            ('st_reserved2', c_long),            
            ('st_reserved3', c_long),            
            ]
    elif _machine == 'ppc':
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('st_ino', c_ulonglong),
            ('st_mode', c_mode_t),
            ('st_nlink', c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    else:
        # i686, use as fallback for everything else
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('__pad1', c_ushort),
            ('__st_ino', c_ulong),
            ('st_mode', c_mode_t),
            ('st_nlink', c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_ino', c_ulonglong)]
else:
    raise NotImplementedError('%s is not supported.' % _system)


class c_statvfs(Structure):
    _fields_ = [
        ('f_bsize', c_ulong),
        ('f_frsize', c_ulong),
        ('f_blocks', c_fsblkcnt_t),
        ('f_bfree', c_fsblkcnt_t),
        ('f_bavail', c_fsblkcnt_t),
        ('f_files', c_fsfilcnt_t),
        ('f_ffree', c_fsfilcnt_t),
        ('f_favail', c_fsfilcnt_t)]

if _system == 'FreeBSD':
    c_fsblkcnt_t = c_uint64
    c_fsfilcnt_t = c_uint64
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t, c_int)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t)
    class c_statvfs(Structure):
        _fields_ = [
            ('f_bavail', c_fsblkcnt_t),
            ('f_bfree', c_fsblkcnt_t),
            ('f_blocks', c_fsblkcnt_t),
            ('f_favail', c_fsfilcnt_t),
            ('f_ffree', c_fsfilcnt_t),
            ('f_files', c_fsfilcnt_t),
            ('f_bsize', c_ulong),
            ('f_flag', c_ulong),
            ('f_frsize', c_ulong)]

class fuse_file_info(Structure):
    _fields_ = [
        ('flags', c_int),
        ('fh_old', c_ulong),
        ('writepage', c_int),
        ('direct_io', c_uint, 1),
        ('keep_cache', c_uint, 1),
        ('flush', c_uint, 1),
        ('padding', c_uint, 29),
        ('fh', c_uint64),
        ('lock_owner', c_uint64)]

class fuse_context(Structure):
    _fields_ = [
        ('fuse', c_voidp),
        ('uid', c_uid_t),
        ('gid', c_gid_t),
        ('pid', c_pid_t),
        ('private_data', c_voidp)]

# Note: parameters do not appear to be current/complete; thus we use fuse_operations_alt
class fuse_operations(Structure):
    _fields_ = [
        ('getattr', CFUNCTYPE(c_int, c_char_p, POINTER(c_stat))),
        ('readlink', CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t)),
        ('mknod', CFUNCTYPE(c_int, c_char_p, c_mode_t, c_dev_t)),
        ('mkdir', CFUNCTYPE(c_int, c_char_p, c_mode_t)),
        ('unlink', CFUNCTYPE(c_int, c_char_p)),
        ('rmdir', CFUNCTYPE(c_int, c_char_p)),
        ('symlink', CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('rename', CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('link', CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('chmod', CFUNCTYPE(c_int, c_char_p, c_mode_t)),
        ('chown', CFUNCTYPE(c_int, c_char_p, c_uid_t, c_gid_t)),
        ('truncate', CFUNCTYPE(c_int, c_char_p, c_off_t)),
        ('open', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))),
        ('read', CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t, c_off_t,
            POINTER(fuse_file_info))),
        ('write', CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t, c_off_t,
            POINTER(fuse_file_info))),
        ('statfs', CFUNCTYPE(c_int, c_char_p, POINTER(c_statvfs))),
        ('flush', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))),
        ('release', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))),
        ('fsync', CFUNCTYPE(c_int, c_char_p, c_int, POINTER(fuse_file_info))),
        ('setxattr', setxattr_t),
        ('getxattr', getxattr_t),
        ('listxattr', CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t)),
        ('removexattr', CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('opendir', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))),
        ('readdir', CFUNCTYPE(c_int, c_char_p, c_voidp, CFUNCTYPE(c_int, c_voidp,
            c_char_p, POINTER(c_stat), c_off_t), c_off_t, POINTER(fuse_file_info))),
        ('releasedir', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))),
        ('fsyncdir', CFUNCTYPE(c_int, c_char_p, c_int, POINTER(fuse_file_info))),
        ('init', CFUNCTYPE(c_voidp, c_voidp)),
        ('destroy', CFUNCTYPE(c_voidp, c_voidp)),
        ('access', CFUNCTYPE(c_int, c_char_p, c_int)),
        ('create', CFUNCTYPE(c_int, c_char_p, c_mode_t, POINTER(fuse_file_info))),
        ('lock', CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info), c_int, c_voidp)),
        ('utimens', CFUNCTYPE(c_int, c_char_p, POINTER(c_utimbuf))),
        ('bmap', CFUNCTYPE(c_int, c_char_p, c_size_t, POINTER(c_ulonglong)))]

class fuse_operations_alt(Structure):
    _fields_ = [
        ('getattr', c_void_p),
        ('readlink', c_void_p),
        ('mknod', c_void_p),
        ('mkdir', c_void_p),
        ('unlink', c_void_p),
        ('rmdir', c_void_p),
        ('symlink', c_void_p),
        ('rename', c_void_p),
        ('link', c_void_p),
        ('chmod', c_void_p),
        ('chown', c_void_p),
        ('truncate', c_void_p),
        ('open', c_void_p),
        ('read', c_void_p),
        ('write', c_void_p),
        ('statfs', c_void_p),
        ('flush', c_void_p),
        ('release', c_void_p),
        ('fsync', c_void_p),
        ('setxattr', c_void_p),
        ('getxattr', c_void_p),
        ('listxattr', c_void_p),
        ('removexattr', c_void_p),
        ('opendir', c_void_p),
        ('readdir', c_void_p),
        ('releasedir', c_void_p),
        ('fsyncdir', c_void_p),
        ('init', c_void_p),
        ('destroy', c_void_p),
        ('access', c_void_p),
        ('create', c_void_p),
        ('lock', c_void_p),
        ('utimens', c_void_p),
        ('bmap', c_void_p)]


def get_vars():
    vars = dict()
    player = (c_char * 256).in_dll(ccode, "player")
    vars['player'] = player
    guard1 = (c_char * 4).in_dll(ccode, "guard1")
    vars['guard1'] = guard1
    player_size = c_ulong.in_dll(ccode, "player_size")
    vars['player_size'] = player_size.value
    solution = (c_char * 128).in_dll(ccode, "solution")
    vars['solution'] = solution
    guard2 = (c_char * 4).in_dll(ccode, "guard2")
    vars['guard2'] = guard2
    status = (c_char * 128).in_dll(ccode, "status")
    vars['status'] = status
    guard3 = (c_char * 4).in_dll(ccode, "guard3")
    vars['guard3'] = guard3
    solution_size = c_ulong.in_dll(ccode, "solution_size")
    vars['solution_size'] = solution_size.value
    guesses = (c_char * 32).in_dll(ccode, "guesses")
    vars['guesses'] = guesses
    guard4 = (c_char * 4).in_dll(ccode, "guard4")
    vars['guard4'] = guard4
    guesses_size = c_ulong.in_dll(ccode, "guesses_size")
    vars['guesses_size'] = guesses_size.value
    return vars
    
def get_var(var):
    vars = get_vars()
    return vars[var]

def is_equal_string(buf, strsize, str, raise_exceptions=True):
    # Gets a byte array (c_char * n) with data of size "strsize" and compares it with string "str"
    bufsize = len(buf)
    assert strsize <= bufsize, 'size of valid data in buffer cannot exceed buffer size'
    strbytes = str.encode()
    assert len(strbytes) <= bufsize, 'size of string to check against exceeds buffer size'
    if strsize != len(strbytes):
        if raise_exceptions:
            raise ValueError(f'String size [{strsize}] is not the length [{len(strbytes)}] of [{str}] as expected')
        return False
    if buf[0:strsize] != strbytes:
        if raise_exceptions:
            raise ValueError(f'String does not match expected string [{str}]')
        return False
    return True

def is_guard_unchanged():
    vars = get_vars()
    if not is_equal_string(vars['guard1'], 4, '123\0'):
        print(vars['guard1'])
        return False
    if not is_equal_string(vars['guard2'], 4, '123\0'):
        print(vars['guard2'])
        return False
    if not is_equal_string(vars['guard3'], 4, '123\0'):
        print(vars['guard3'])
        return False
    if not is_equal_string(vars['guard4'], 4, '123\0'):
        print(vars['guard4'])
        return False
    return True

def set_int(var, value):
    """value range: 0..255"""
    addr = addressof(c_ulong.in_dll(ccode, var))
    memset(addr, value, 1)
    assert c_ulong.in_dll(ccode, var).value == value

def set_str(var, maxsize, value):
    assert len(value) <= maxsize
    addr = addressof(c_ulong.in_dll(ccode, var))
    for i, c in enumerate(value):
        memset(addr + i, ord(c), 1)
    cchars = (c_char * maxsize).in_dll(ccode, var)
    assert is_equal_string(cchars, len(value), value, raise_exceptions=True)

def set_var(var, value):
    if var == 'player':
        set_str(var, 256, value)
    elif var == 'player_size':
        set_int(var, value)
    elif var == 'solution':
        set_str(var, 128, value)
    elif var == 'status':
        set_str(var, 128, value)
    elif var == 'solution_size':
        set_int(var, value)
    elif var == 'guesses':
        set_str(var, 32, value)
    elif var == 'guesses_size':
        set_int(var, value)
    else:
        assert False, 'unknown variable'

def call_getattr(path):
    fs_getattr = ccode.fs_getattr
    fs_getattr.argtypes = c_char_p, POINTER(c_stat), POINTER(fuse_file_info)
    fs_getattr.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)
    stat = c_stat()
    ffi = fuse_file_info()
    ret = fs_getattr(path.value, stat, ffi)
    return ret, stat

def call_readdir(path):
    files = set()

    #typedef int (*fuse_fill_dir_t) (void *buf, const char *name, const struct stat *stbuf, off_t off, enum fuse_fill_dir_flags flags);
    def py_filler_func(buf, name, stbuf, off, fill_dir_flags):
        files.add(name)
        return 0

    c_fuse_fill_dir_t = CFUNCTYPE(c_int, c_char_p, c_char_p, c_char_p, c_off_t, c_int)
    fuse_fill_dir = c_fuse_fill_dir_t(py_filler_func)
    
    fs_readdir = ccode.fs_readdir
    # int fs_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi, enum fuse_readdir_flags flags)
    fs_readdir.argtypes = c_char_p, c_char_p, c_fuse_fill_dir_t, c_off_t, c_char_p, c_int
    fs_readdir.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)
    buf = create_string_buffer(b'dummy',size=10)
    offset = 0
    fi = None
    flags = 0
    ret = fs_readdir(path.value, buf, fuse_fill_dir, offset, fi, flags)
    files = { file.decode() for file in files }
    return ret, files

def call_open(path, flags):
    fs_open = ccode.fs_open
    fs_open.argtypes = c_char_p, POINTER(fuse_file_info)
    fs_open.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)
    ffi = fuse_file_info()
    ffi.flags = flags
    ret = fs_open(path.value, ffi)
    return ret

def call_read(path, buf, size, offset):
    fs_read = ccode.fs_read
    fs_read.argtypes = c_char_p, POINTER(c_byte), c_size_t, c_off_t, POINTER(fuse_file_info)
    fs_read.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)    
    ffi = fuse_file_info()
    ret_size = fs_read(path.value, buf, size, offset, ffi)
    return ret_size

def call_truncate(path, offset):
    fs_truncate = ccode.fs_truncate
    fs_truncate.argtypes = c_char_p, c_off_t, POINTER(fuse_file_info)
    fs_truncate.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)
    ffi = fuse_file_info()
    ret = fs_truncate(path.value, offset, None)
    return ret

def call_write(path, buf, size, offset):
    fs_write = ccode.fs_write
    fs_write.argtypes = c_char_p, POINTER(c_byte), c_size_t, c_off_t, POINTER(fuse_file_info)
    fs_write.restype = c_int
    path = create_string_buffer(path.encode('ascii'), size=50)    
    ffi = fuse_file_info()
    ret_size = fs_write(path.value, buf, size, offset, ffi)
    return ret_size

def read_file(path):
    #buf = create_string_buffer(b'', size=256)
    #buf = (c_byte * 256).from_buffer(buf)
    buf = (c_byte * 256)()
    size = call_read(path, buf, 256, 0)
    if size < 0:
        return None
    content = bytearray(buf).decode('ascii')  
    print(size, content)    
    return content[0:size]

def write_file(path, content):
    buf = create_string_buffer(content.encode('ascii'), size=len(content))
    buf = (c_byte * len(content)).from_buffer(buf)
    return call_write(path, buf, len(content), 0)

def append_file(path, content):
    ret, stat = call_getattr(path)
    size = stat.st_size
    buf = create_string_buffer(content.encode('ascii'), size=len(content))
    buf = (c_byte * len(content)).from_buffer(buf)
    return call_write(path, buf, len(content), size)
