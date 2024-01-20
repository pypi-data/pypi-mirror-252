# -*- coding: utf-8 -*-

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Test utilities."""

from __future__ import print_function

import atexit
import contextlib
import ctypes
import errno
import functools
import gc
import inspect
import os
import platform
import random
import re
import select
import shlex
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
import warnings
from socket import AF_INET
from socket import AF_INET6
from socket import SOCK_STREAM

import psutil
from psutil import AIX
from psutil import LINUX
from psutil import MACOS
from psutil import NETBSD
from psutil import OPENBSD
from psutil import POSIX
from psutil import SUNOS
from psutil import WINDOWS
from psutil._common import bytes2human
from psutil._common import debug
from psutil._common import memoize
from psutil._common import print_color
from psutil._common import supports_ipv6
from psutil._compat import PY3
from psutil._compat import FileExistsError
from psutil._compat import FileNotFoundError
from psutil._compat import range
from psutil._compat import super
from psutil._compat import u
from psutil._compat import unicode
from psutil._compat import which


try:
    from unittest import mock  # py3
except ImportError:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import mock  # NOQA - requires "pip install mock"

if PY3:
    import enum
else:
    enum = None

if POSIX:
    from psutil._psposix import wait_pid


# fmt: off
__all__ = [
    # constants
    'APPVEYOR', 'DEVNULL', 'GLOBAL_TIMEOUT', 'TOLERANCE_SYS_MEM', 'NO_RETRIES',
    'PYPY', 'PYTHON_EXE', 'PYTHON_EXE_ENV', 'ROOT_DIR', 'SCRIPTS_DIR',
    'TESTFN_PREFIX', 'UNICODE_SUFFIX', 'INVALID_UNICODE_SUFFIX',
    'CI_TESTING', 'VALID_PROC_STATUSES', 'TOLERANCE_DISK_USAGE', 'IS_64BIT',
    "HAS_CPU_AFFINITY", "HAS_CPU_FREQ", "HAS_ENVIRON", "HAS_PROC_IO_COUNTERS",
    "HAS_IONICE", "HAS_MEMORY_MAPS", "HAS_PROC_CPU_NUM", "HAS_RLIMIT",
    "HAS_SENSORS_BATTERY", "HAS_BATTERY", "HAS_SENSORS_FANS",
    "HAS_SENSORS_TEMPERATURES", "MACOS_11PLUS",
    "MACOS_12PLUS", "COVERAGE",
    # subprocesses
    'pyrun', 'terminate', 'reap_children', 'spawn_testproc', 'spawn_zombie',
    'spawn_children_pair',
    # threads
    'ThreadTask',
    # test utils
    'unittest', 'skip_on_access_denied', 'skip_on_not_implemented',
    'retry_on_failure', 'TestMemoryLeak', 'PsutilTestCase',
    'process_namespace', 'system_namespace', 'print_sysinfo',
    'is_win_secure_system_proc',
    # fs utils
    'chdir', 'safe_rmpath', 'create_py_exe', 'create_c_exe', 'get_testfn',
    # os
    'get_winver', 'kernel_version',
    # sync primitives
    'call_until', 'wait_for_pid', 'wait_for_file',
    # network
    'check_net_address', 'filter_proc_connections',
    'get_free_port', 'bind_socket', 'bind_unix_socket', 'tcp_socketpair',
    'unix_socketpair', 'create_sockets',
    # compat
    'reload_module', 'import_module_by_path',
    # others
    'warn', 'copyload_shared_lib', 'is_namedtuple',
]
# fmt: on


# ===================================================================
# --- constants
# ===================================================================

# --- platforms

PYPY = '__pypy__' in sys.builtin_module_names
# whether we're running this test suite on a Continuous Integration service
APPVEYOR = 'APPVEYOR' in os.environ
GITHUB_ACTIONS = 'GITHUB_ACTIONS' in os.environ or 'CIBUILDWHEEL' in os.environ
CI_TESTING = APPVEYOR or GITHUB_ACTIONS
COVERAGE = 'COVERAGE_RUN' in os.environ
# are we a 64 bit process?
IS_64BIT = sys.maxsize > 2**32


@memoize
def macos_version():
    version_str = platform.mac_ver()[0]
    version = tuple(map(int, version_str.split(".")[:2]))
    if version == (10, 16):
        # When built against an older macOS SDK, Python will report
        # macOS 10.16 instead of the real version.
        version_str = subprocess.check_output(
            [
                sys.executable,
                "-sS",
                "-c",
                "import platform; print(platform.mac_ver()[0])",
            ],
            env={"SYSTEM_VERSION_COMPAT": "0"},
            universal_newlines=True,
        )
        version = tuple(map(int, version_str.split(".")[:2]))
    return version


if MACOS:
    MACOS_11PLUS = macos_version() > (10, 15)
    MACOS_12PLUS = macos_version() >= (12, 0)
else:
    MACOS_11PLUS = False
    MACOS_12PLUS = False


# --- configurable defaults

# how many times retry_on_failure() decorator will retry
NO_RETRIES = 10
# bytes tolerance for system-wide related tests
TOLERANCE_SYS_MEM = 5 * 1024 * 1024  # 5MB
TOLERANCE_DISK_USAGE = 10 * 1024 * 1024  # 10MB
# the timeout used in functions which have to wait
GLOBAL_TIMEOUT = 5
# be more tolerant if we're on CI in order to avoid false positives
if CI_TESTING:
    NO_RETRIES *= 3
    GLOBAL_TIMEOUT *= 3
    TOLERANCE_SYS_MEM *= 4
    TOLERANCE_DISK_USAGE *= 3

# --- file names

# Disambiguate TESTFN for parallel testing.
if os.name == 'java':
    # Jython disallows @ in module names
    TESTFN_PREFIX = '$psutil-%s-' % os.getpid()
else:
    TESTFN_PREFIX = '@psutil-%s-' % os.getpid()
UNICODE_SUFFIX = u("-ƒőő")
# An invalid unicode string.
if PY3:
    INVALID_UNICODE_SUFFIX = b"f\xc0\x80".decode('utf8', 'surrogateescape')
else:
    INVALID_UNICODE_SUFFIX = "f\xc0\x80"
ASCII_FS = sys.getfilesystemencoding().lower() in ('ascii', 'us-ascii')

# --- paths

ROOT_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
SCRIPTS_DIR = os.environ.get(
    "PSUTIL_SCRIPTS_DIR", os.path.join(ROOT_DIR, 'scripts')
)
HERE = os.path.realpath(os.path.dirname(__file__))

# --- support

HAS_CONNECTIONS_UNIX = POSIX and not SUNOS
HAS_CPU_AFFINITY = hasattr(psutil.Process, "cpu_affinity")
HAS_CPU_FREQ = hasattr(psutil, "cpu_freq")
HAS_GETLOADAVG = hasattr(psutil, "getloadavg")
HAS_ENVIRON = hasattr(psutil.Process, "environ")
HAS_IONICE = hasattr(psutil.Process, "ionice")
HAS_MEMORY_MAPS = hasattr(psutil.Process, "memory_maps")
HAS_NET_IO_COUNTERS = hasattr(psutil, "net_io_counters")
HAS_PROC_CPU_NUM = hasattr(psutil.Process, "cpu_num")
HAS_PROC_IO_COUNTERS = hasattr(psutil.Process, "io_counters")
HAS_RLIMIT = hasattr(psutil.Process, "rlimit")
HAS_SENSORS_BATTERY = hasattr(psutil, "sensors_battery")
try:
    HAS_BATTERY = HAS_SENSORS_BATTERY and bool(psutil.sensors_battery())
except Exception:  # noqa: BLE001
    HAS_BATTERY = False
HAS_SENSORS_FANS = hasattr(psutil, "sensors_fans")
HAS_SENSORS_TEMPERATURES = hasattr(psutil, "sensors_temperatures")
HAS_THREADS = hasattr(psutil.Process, "threads")
SKIP_SYSCONS = (MACOS or AIX) and os.getuid() != 0

# --- misc


def _get_py_exe():
    def attempt(exe):
        try:
            subprocess.check_call(
                [exe, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            return None
        else:
            return exe

    env = os.environ.copy()

    # On Windows, starting with python 3.7, virtual environments use a
    # venv launcher startup process. This does not play well when
    # counting spawned processes, or when relying on the PID of the
    # spawned process to do some checks, e.g. connections check per PID.
    # Let's use the base python in this case.
    base = getattr(sys, "_base_executable", None)
    if WINDOWS and sys.version_info >= (3, 7) and base is not None:
        # We need to set __PYVENV_LAUNCHER__ to sys.executable for the
        # base python executable to know about the environment.
        env["__PYVENV_LAUNCHER__"] = sys.executable
        return base, env
    elif GITHUB_ACTIONS:
        return sys.executable, env
    elif MACOS:
        exe = (
            attempt(sys.executable)
            or attempt(os.path.realpath(sys.executable))
            or attempt(which("python%s.%s" % sys.version_info[:2]))
            or attempt(psutil.Process().exe())
        )
        if not exe:
            raise ValueError("can't find python exe real abspath")
        return exe, env
    else:
        exe = os.path.realpath(sys.executable)
        assert os.path.exists(exe), exe
        return exe, env


PYTHON_EXE, PYTHON_EXE_ENV = _get_py_exe()
DEVNULL = open(os.devnull, 'r+')
atexit.register(DEVNULL.close)

VALID_PROC_STATUSES = [
    getattr(psutil, x) for x in dir(psutil) if x.startswith('STATUS_')
]
AF_UNIX = getattr(socket, "AF_UNIX", object())

_subprocesses_started = set()
_pids_started = set()


# ===================================================================
# --- threads
# ===================================================================


class ThreadTask(threading.Thread):
    """A thread task which does nothing expect staying alive."""

    def __init__(self):
        super().__init__()
        self._running = False
        self._interval = 0.001
        self._flag = threading.Event()

    def __repr__(self):
        name = self.__class__.__name__
        return '<%s running=%s at %#x>' % (name, self._running, id(self))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()

    def start(self):
        """Start thread and keep it running until an explicit
        stop() request. Polls for shutdown every 'timeout' seconds.
        """
        if self._running:
            raise ValueError("already started")
        threading.Thread.start(self)
        self._flag.wait()

    def run(self):
        self._running = True
        self._flag.set()
        while self._running:
            time.sleep(self._interval)

    def stop(self):
        """Stop thread execution and and waits until it is stopped."""
        if not self._running:
            raise ValueError("already stopped")
        self._running = False
        self.join()


# ===================================================================
# --- subprocesses
# ===================================================================


def _reap_children_on_err(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception:
            reap_children()
            raise

    return wrapper


@_reap_children_on_err
def spawn_testproc(cmd=None, **kwds):
    """Create a python subprocess which does nothing for some secs and
    return it as a subprocess.Popen instance.
    If "cmd" is specified that is used instead of python.
    By default stdin and stdout are redirected to /dev/null.
    It also attempts to make sure the process is in a reasonably
    initialized state.
    The process is registered for cleanup on reap_children().
    """
    kwds.setdefault("stdin", DEVNULL)
    kwds.setdefault("stdout", DEVNULL)
    kwds.setdefault("cwd", os.getcwd())
    kwds.setdefault("env", PYTHON_EXE_ENV)
    if WINDOWS:
        # Prevents the subprocess to open error dialogs. This will also
        # cause stderr to be suppressed, which is suboptimal in order
        # to debug broken tests.
        CREATE_NO_WINDOW = 0x8000000
        kwds.setdefault("creationflags", CREATE_NO_WINDOW)
    if cmd is None:
        testfn = get_testfn(dir=os.getcwd())
        try:
            safe_rmpath(testfn)
            pyline = (
                "import time;"
                + "open(r'%s', 'w').close();" % testfn
                + "[time.sleep(0.1) for x in range(100)];"  # 10 secs
            )
            cmd = [PYTHON_EXE, "-c", pyline]
            sproc = subprocess.Popen(cmd, **kwds)
            _subprocesses_started.add(sproc)
            wait_for_file(testfn, delete=True, empty=True)
        finally:
            safe_rmpath(testfn)
    else:
        sproc = subprocess.Popen(cmd, **kwds)
        _subprocesses_started.add(sproc)
        wait_for_pid(sproc.pid)
    return sproc


@_reap_children_on_err
def spawn_children_pair():
    """Create a subprocess which creates another one as in:
    A (us) -> B (child) -> C (grandchild).
    Return a (child, grandchild) tuple.
    The 2 processes are fully initialized and will live for 60 secs
    and are registered for cleanup on reap_children().
    """
    tfile = None
    testfn = get_testfn(dir=os.getcwd())
    try:
        s = textwrap.dedent("""\
            import subprocess, os, sys, time
            s = "import os, time;"
            s += "f = open('%s', 'w');"
            s += "f.write(str(os.getpid()));"
            s += "f.close();"
            s += "time.sleep(60);"
            p = subprocess.Popen([r'%s', '-c', s])
            p.wait()
            """ % (os.path.basename(testfn), PYTHON_EXE))
        # On Windows if we create a subprocess with CREATE_NO_WINDOW flag
        # set (which is the default) a "conhost.exe" extra process will be
        # spawned as a child. We don't want that.
        if WINDOWS:
            subp, tfile = pyrun(s, creationflags=0)
        else:
            subp, tfile = pyrun(s)
        child = psutil.Process(subp.pid)
        grandchild_pid = int(wait_for_file(testfn, delete=True, empty=False))
        _pids_started.add(grandchild_pid)
        grandchild = psutil.Process(grandchild_pid)
        return (child, grandchild)
    finally:
        safe_rmpath(testfn)
        if tfile is not None:
            safe_rmpath(tfile)


def spawn_zombie():
    """Create a zombie process and return a (parent, zombie) process tuple.
    In order to kill the zombie parent must be terminate()d first, then
    zombie must be wait()ed on.
    """
    assert psutil.POSIX
    unix_file = get_testfn()
    src = textwrap.dedent("""\
        import os, sys, time, socket, contextlib
        child_pid = os.fork()
        if child_pid > 0:
            time.sleep(3000)
        else:
            # this is the zombie process
            s = socket.socket(socket.AF_UNIX)
            with contextlib.closing(s):
                s.connect('%s')
                if sys.version_info < (3, ):
                    pid = str(os.getpid())
                else:
                    pid = bytes(str(os.getpid()), 'ascii')
                s.sendall(pid)
        """ % unix_file)
    tfile = None
    sock = bind_unix_socket(unix_file)
    try:
        sock.settimeout(GLOBAL_TIMEOUT)
        parent, tfile = pyrun(src)
        conn, _ = sock.accept()
        try:
            select.select([conn.fileno()], [], [], GLOBAL_TIMEOUT)
            zpid = int(conn.recv(1024))
            _pids_started.add(zpid)
            zombie = psutil.Process(zpid)
            call_until(zombie.status, "ret == psutil.STATUS_ZOMBIE")
            return (parent, zombie)
        finally:
            conn.close()
    finally:
        sock.close()
        safe_rmpath(unix_file)
        if tfile is not None:
            safe_rmpath(tfile)


@_reap_children_on_err
def pyrun(src, **kwds):
    """Run python 'src' code string in a separate interpreter.
    Returns a subprocess.Popen instance and the test file where the source
    code was written.
    """
    kwds.setdefault("stdout", None)
    kwds.setdefault("stderr", None)
    srcfile = get_testfn()
    try:
        with open(srcfile, "w") as f:
            f.write(src)
        subp = spawn_testproc([PYTHON_EXE, f.name], **kwds)
        wait_for_pid(subp.pid)
        return (subp, srcfile)
    except Exception:
        safe_rmpath(srcfile)
        raise


@_reap_children_on_err
def sh(cmd, **kwds):
    """Run cmd in a subprocess and return its output.
    raises RuntimeError on error.
    """
    # Prevents subprocess to open error dialogs in case of error.
    flags = 0x8000000 if WINDOWS else 0
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.PIPE)
    kwds.setdefault("universal_newlines", True)
    kwds.setdefault("creationflags", flags)
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    p = subprocess.Popen(cmd, **kwds)
    _subprocesses_started.add(p)
    if PY3:
        stdout, stderr = p.communicate(timeout=GLOBAL_TIMEOUT)
    else:
        stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(stderr)
    if stderr:
        warn(stderr)
    if stdout.endswith('\n'):
        stdout = stdout[:-1]
    return stdout


def terminate(proc_or_pid, sig=signal.SIGTERM, wait_timeout=GLOBAL_TIMEOUT):
    """Terminate a process and wait() for it.
    Process can be a PID or an instance of psutil.Process(),
    subprocess.Popen() or psutil.Popen().
    If it's a subprocess.Popen() or psutil.Popen() instance also closes
    its stdin / stdout / stderr fds.
    PID is wait()ed even if the process is already gone (kills zombies).
    Does nothing if the process does not exist.
    Return process exit status.
    """

    def wait(proc, timeout):
        if isinstance(proc, subprocess.Popen) and not PY3:
            proc.wait()
        else:
            proc.wait(timeout)
        if WINDOWS and isinstance(proc, subprocess.Popen):
            # Otherwise PID may still hang around.
            try:
                return psutil.Process(proc.pid).wait(timeout)
            except psutil.NoSuchProcess:
                pass

    def sendsig(proc, sig):
        # XXX: otherwise the build hangs for some reason.
        if MACOS and GITHUB_ACTIONS:
            sig = signal.SIGKILL
        # If the process received SIGSTOP, SIGCONT is necessary first,
        # otherwise SIGTERM won't work.
        if POSIX and sig != signal.SIGKILL:
            proc.send_signal(signal.SIGCONT)
        proc.send_signal(sig)

    def term_subprocess_proc(proc, timeout):
        try:
            sendsig(proc, sig)
        except OSError as err:
            if WINDOWS and err.winerror == 6:  # "invalid handle"
                pass
            elif err.errno != errno.ESRCH:
                raise
        return wait(proc, timeout)

    def term_psutil_proc(proc, timeout):
        try:
            sendsig(proc, sig)
        except psutil.NoSuchProcess:
            pass
        return wait(proc, timeout)

    def term_pid(pid, timeout):
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            # Needed to kill zombies.
            if POSIX:
                return wait_pid(pid, timeout)
        else:
            return term_psutil_proc(proc, timeout)

    def flush_popen(proc):
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        # Flushing a BufferedWriter may raise an error.
        if proc.stdin:
            proc.stdin.close()

    p = proc_or_pid
    try:
        if isinstance(p, int):
            return term_pid(p, wait_timeout)
        elif isinstance(p, (psutil.Process, psutil.Popen)):
            return term_psutil_proc(p, wait_timeout)
        elif isinstance(p, subprocess.Popen):
            return term_subprocess_proc(p, wait_timeout)
        else:
            raise TypeError("wrong type %r" % p)
    finally:
        if isinstance(p, (subprocess.Popen, psutil.Popen)):
            flush_popen(p)
        pid = p if isinstance(p, int) else p.pid
        assert not psutil.pid_exists(pid), pid


def reap_children(recursive=False):
    """Terminate and wait() any subprocess started by this test suite
    and any children currently running, ensuring that no processes stick
    around to hog resources.
    If recursive is True it also tries to terminate and wait()
    all grandchildren started by this process.
    """
    # Get the children here before terminating them, as in case of
    # recursive=True we don't want to lose the intermediate reference
    # pointing to the grandchildren.
    children = psutil.Process().children(recursive=recursive)

    # Terminate subprocess.Popen.
    while _subprocesses_started:
        subp = _subprocesses_started.pop()
        terminate(subp)

    # Collect started pids.
    while _pids_started:
        pid = _pids_started.pop()
        terminate(pid)

    # Terminate children.
    if children:
        for p in children:
            terminate(p, wait_timeout=None)
        _, alive = psutil.wait_procs(children, timeout=GLOBAL_TIMEOUT)
        for p in alive:
            warn("couldn't terminate process %r; attempting kill()" % p)
            terminate(p, sig=signal.SIGKILL)


# ===================================================================
# --- OS
# ===================================================================


def kernel_version():
    """Return a tuple such as (2, 6, 36)."""
    if not POSIX:
        raise NotImplementedError("not POSIX")
    s = ""
    uname = os.uname()[2]
    for c in uname:
        if c.isdigit() or c == '.':
            s += c
        else:
            break
    if not s:
        raise ValueError("can't parse %r" % uname)
    minor = 0
    micro = 0
    nums = s.split('.')
    major = int(nums[0])
    if len(nums) >= 2:
        minor = int(nums[1])
    if len(nums) >= 3:
        micro = int(nums[2])
    return (major, minor, micro)


def get_winver():
    if not WINDOWS:
        raise NotImplementedError("not WINDOWS")
    wv = sys.getwindowsversion()
    if hasattr(wv, 'service_pack_major'):  # python >= 2.7
        sp = wv.service_pack_major or 0
    else:
        r = re.search(r"\s\d$", wv[4])
        sp = int(r.group(0)) if r else 0
    return (wv[0], wv[1], sp)


# ===================================================================
# --- sync primitives
# ===================================================================


class retry:
    """A retry decorator."""

    def __init__(
        self,
        exception=Exception,
        timeout=None,
        retries=None,
        interval=0.001,
        logfun=None,
    ):
        if timeout and retries:
            raise ValueError("timeout and retries args are mutually exclusive")
        self.exception = exception
        self.timeout = timeout
        self.retries = retries
        self.interval = interval
        self.logfun = logfun

    def __iter__(self):
        if self.timeout:
            stop_at = time.time() + self.timeout
            while time.time() < stop_at:
                yield
        elif self.retries:
            for _ in range(self.retries):
                yield
        else:
            while True:
                yield

    def sleep(self):
        if self.interval is not None:
            time.sleep(self.interval)

    def __call__(self, fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            exc = None
            for _ in self:
                try:
                    return fun(*args, **kwargs)
                except self.exception as _:  # NOQA
                    exc = _
                    if self.logfun is not None:
                        self.logfun(exc)
                    self.sleep()
                    continue
            if PY3:
                raise exc
            else:
                raise

        # This way the user of the decorated function can change config
        # parameters.
        wrapper.decorator = self
        return wrapper


@retry(
    exception=psutil.NoSuchProcess,
    logfun=None,
    timeout=GLOBAL_TIMEOUT,
    interval=0.001,
)
def wait_for_pid(pid):
    """Wait for pid to show up in the process list then return.
    Used in the test suite to give time the sub process to initialize.
    """
    if pid not in psutil.pids():
        raise psutil.NoSuchProcess(pid)
    psutil.Process(pid)


@retry(
    exception=(FileNotFoundError, AssertionError),
    logfun=None,
    timeout=GLOBAL_TIMEOUT,
    interval=0.001,
)
def wait_for_file(fname, delete=True, empty=False):
    """Wait for a file to be written on disk with some content."""
    with open(fname, "rb") as f:
        data = f.read()
    if not empty:
        assert data
    if delete:
        safe_rmpath(fname)
    return data


@retry(
    exception=AssertionError,
    logfun=None,
    timeout=GLOBAL_TIMEOUT,
    interval=0.001,
)
def call_until(fun, expr):
    """Keep calling function for timeout secs and exit if eval()
    expression is True.
    """
    ret = fun()
    assert eval(expr)  # noqa
    return ret


# ===================================================================
# --- fs
# ===================================================================


def safe_rmpath(path):
    """Convenience function for removing temporary test files or dirs."""

    def retry_fun(fun):
        # On Windows it could happen that the file or directory has
        # open handles or references preventing the delete operation
        # to succeed immediately, so we retry for a while. See:
        # https://bugs.python.org/issue33240
        stop_at = time.time() + GLOBAL_TIMEOUT
        while time.time() < stop_at:
            try:
                return fun()
            except FileNotFoundError:
                pass
            except WindowsError as _:
                err = _
                warn("ignoring %s" % (str(err)))
            time.sleep(0.01)
        raise err

    try:
        st = os.stat(path)
        if stat.S_ISDIR(st.st_mode):
            fun = functools.partial(shutil.rmtree, path)
        else:
            fun = functools.partial(os.remove, path)
        if POSIX:
            fun()
        else:
            retry_fun(fun)
    except FileNotFoundError:
        pass


def safe_mkdir(dir):
    """Convenience function for creating a directory."""
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass


@contextlib.contextmanager
def chdir(dirname):
    """Context manager which temporarily changes the current directory."""
    curdir = os.getcwd()
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def create_py_exe(path):
    """Create a Python executable file in the given location."""
    assert not os.path.exists(path), path
    atexit.register(safe_rmpath, path)
    shutil.copyfile(PYTHON_EXE, path)
    if POSIX:
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)
    return path


def create_c_exe(path, c_code=None):
    """Create a compiled C executable in the given location."""
    assert not os.path.exists(path), path
    if not which("gcc"):
        raise unittest.SkipTest("gcc is not installed")
    if c_code is None:
        c_code = textwrap.dedent("""
            #include <unistd.h>
            int main() {
                pause();
                return 1;
            }
            """)
    else:
        assert isinstance(c_code, str), c_code

    atexit.register(safe_rmpath, path)
    with open(get_testfn(suffix='.c'), "w") as f:
        f.write(c_code)
    try:
        subprocess.check_call(["gcc", f.name, "-o", path])
    finally:
        safe_rmpath(f.name)
    return path


def get_testfn(suffix="", dir=None):
    """Return an absolute pathname of a file or dir that did not
    exist at the time this call is made. Also schedule it for safe
    deletion at interpreter exit. It's technically racy but probably
    not really due to the time variant.
    """
    while True:
        name = tempfile.mktemp(prefix=TESTFN_PREFIX, suffix=suffix, dir=dir)
        if not os.path.exists(name):  # also include dirs
            path = os.path.realpath(name)  # needed for OSX
            atexit.register(safe_rmpath, path)
            return path


# ===================================================================
# --- testing
# ===================================================================


class TestCase(unittest.TestCase):

    # Print a full path representation of the single unit tests
    # being run.
    def __str__(self):
        fqmod = self.__class__.__module__
        if not fqmod.startswith('psutil.'):
            fqmod = 'psutil.tests.' + fqmod
        return "%s.%s.%s" % (
            fqmod,
            self.__class__.__name__,
            self._testMethodName,
        )

    # assertRaisesRegexp renamed to assertRaisesRegex in 3.3;
    # add support for the new name.
    if not hasattr(unittest.TestCase, 'assertRaisesRegex'):
        assertRaisesRegex = unittest.TestCase.assertRaisesRegexp  # noqa

    # ...otherwise multiprocessing.Pool complains
    if not PY3:

        def runTest(self):
            pass

        @contextlib.contextmanager
        def subTest(self, *args, **kw):
            # fake it for python 2.7
            yield


# monkey patch default unittest.TestCase
unittest.TestCase = TestCase


class PsutilTestCase(TestCase):
    """Test class providing auto-cleanup wrappers on top of process
    test utilities.
    """

    def get_testfn(self, suffix="", dir=None):
        fname = get_testfn(suffix=suffix, dir=dir)
        self.addCleanup(safe_rmpath, fname)
        return fname

    def spawn_testproc(self, *args, **kwds):
        sproc = spawn_testproc(*args, **kwds)
        self.addCleanup(terminate, sproc)
        return sproc

    def spawn_children_pair(self):
        child1, child2 = spawn_children_pair()
        self.addCleanup(terminate, child2)
        self.addCleanup(terminate, child1)  # executed first
        return (child1, child2)

    def spawn_zombie(self):
        parent, zombie = spawn_zombie()
        self.addCleanup(terminate, zombie)
        self.addCleanup(terminate, parent)  # executed first
        return (parent, zombie)

    def pyrun(self, *args, **kwds):
        sproc, srcfile = pyrun(*args, **kwds)
        self.addCleanup(safe_rmpath, srcfile)
        self.addCleanup(terminate, sproc)  # executed first
        return sproc

    def _check_proc_exc(self, proc, exc):
        self.assertIsInstance(exc, psutil.Error)
        self.assertEqual(exc.pid, proc.pid)
        self.assertEqual(exc.name, proc._name)
        if exc.name:
            self.assertNotEqual(exc.name, "")
        if isinstance(exc, psutil.ZombieProcess):
            self.assertEqual(exc.ppid, proc._ppid)
            if exc.ppid is not None:
                self.assertGreaterEqual(exc.ppid, 0)
        str(exc)
        repr(exc)

    def assertPidGone(self, pid):
        with self.assertRaises(psutil.NoSuchProcess) as cm:
            try:
                psutil.Process(pid)
            except psutil.ZombieProcess:
                raise AssertionError("wasn't supposed to raise ZombieProcess")
        self.assertEqual(cm.exception.pid, pid)
        self.assertEqual(cm.exception.name, None)
        assert not psutil.pid_exists(pid), pid
        self.assertNotIn(pid, psutil.pids())
        self.assertNotIn(pid, [x.pid for x in psutil.process_iter()])

    def assertProcessGone(self, proc):
        self.assertPidGone(proc.pid)
        ns = process_namespace(proc)
        for fun, name in ns.iter(ns.all, clear_cache=True):
            with self.subTest(proc=proc, name=name):
                try:
                    ret = fun()
                except psutil.ZombieProcess:
                    raise
                except psutil.NoSuchProcess as exc:
                    self._check_proc_exc(proc, exc)
                else:
                    msg = "Process.%s() didn't raise NSP and returned %r" % (
                        name,
                        ret,
                    )
                    raise AssertionError(msg)
        proc.wait(timeout=0)  # assert not raise TimeoutExpired

    def assertProcessZombie(self, proc):
        # A zombie process should always be instantiable.
        clone = psutil.Process(proc.pid)
        # Cloned zombie on Open/NetBSD has null creation time, see:
        # https://github.com/giampaolo/psutil/issues/2287
        self.assertEqual(proc, clone)
        if not (OPENBSD or NETBSD):
            self.assertEqual(hash(proc), hash(clone))
        # Its status always be querable.
        self.assertEqual(proc.status(), psutil.STATUS_ZOMBIE)
        # It should be considered 'running'.
        assert proc.is_running()
        assert psutil.pid_exists(proc.pid)
        # as_dict() shouldn't crash.
        proc.as_dict()
        # It should show up in pids() and process_iter().
        self.assertIn(proc.pid, psutil.pids())
        self.assertIn(proc.pid, [x.pid for x in psutil.process_iter()])
        psutil._pmap = {}
        self.assertIn(proc.pid, [x.pid for x in psutil.process_iter()])
        # Call all methods.
        ns = process_namespace(proc)
        for fun, name in ns.iter(ns.all, clear_cache=True):
            with self.subTest(proc=proc, name=name):
                try:
                    fun()
                except (psutil.ZombieProcess, psutil.AccessDenied) as exc:
                    self._check_proc_exc(proc, exc)
        if LINUX:
            # https://github.com/giampaolo/psutil/pull/2288
            with self.assertRaises(psutil.ZombieProcess) as cm:
                proc.cmdline()
            self._check_proc_exc(proc, cm.exception)
            with self.assertRaises(psutil.ZombieProcess) as cm:
                proc.exe()
            self._check_proc_exc(proc, cm.exception)
            with self.assertRaises(psutil.ZombieProcess) as cm:
                proc.memory_maps()
            self._check_proc_exc(proc, cm.exception)
        # Zombie cannot be signaled or terminated.
        proc.suspend()
        proc.resume()
        proc.terminate()
        proc.kill()
        assert proc.is_running()
        assert psutil.pid_exists(proc.pid)
        self.assertIn(proc.pid, psutil.pids())
        self.assertIn(proc.pid, [x.pid for x in psutil.process_iter()])
        psutil._pmap = {}
        self.assertIn(proc.pid, [x.pid for x in psutil.process_iter()])

        # Its parent should 'see' it (edit: not true on BSD and MACOS).
        # descendants = [x.pid for x in psutil.Process().children(
        #                recursive=True)]
        # self.assertIn(proc.pid, descendants)

        # __eq__ can't be relied upon because creation time may not be
        # querable.
        # self.assertEqual(proc, psutil.Process(proc.pid))

        # XXX should we also assume ppid() to be usable? Note: this
        # would be an important use case as the only way to get
        # rid of a zombie is to kill its parent.
        # self.assertEqual(proc.ppid(), os.getpid())


@unittest.skipIf(PYPY, "unreliable on PYPY")
class TestMemoryLeak(PsutilTestCase):
    """Test framework class for detecting function memory leaks,
    typically functions implemented in C which forgot to free() memory
    from the heap. It does so by checking whether the process memory
    usage increased before and after calling the function many times.

    Note that this is hard (probably impossible) to do reliably, due
    to how the OS handles memory, the GC and so on (memory can even
    decrease!). In order to avoid false positives, in case of failure
    (mem > 0) we retry the test for up to 5 times, increasing call
    repetitions each time. If the memory keeps increasing then it's a
    failure.

    If available (Linux, OSX, Windows), USS memory is used for comparison,
    since it's supposed to be more precise, see:
    https://gmpy.dev/blog/2016/real-process-memory-and-environ-in-python
    If not, RSS memory is used. mallinfo() on Linux and _heapwalk() on
    Windows may give even more precision, but at the moment are not
    implemented.

    PyPy appears to be completely unstable for this framework, probably
    because of its JIT, so tests on PYPY are skipped.

    Usage:

        class TestLeaks(psutil.tests.TestMemoryLeak):

            def test_fun(self):
                self.execute(some_function)
    """

    # Configurable class attrs.
    times = 200
    warmup_times = 10
    tolerance = 0  # memory
    retries = 10 if CI_TESTING else 5
    verbose = True
    _thisproc = psutil.Process()
    _psutil_debug_orig = bool(os.getenv('PSUTIL_DEBUG'))

    @classmethod
    def setUpClass(cls):
        psutil._set_debug(False)  # avoid spamming to stderr

    @classmethod
    def tearDownClass(cls):
        psutil._set_debug(cls._psutil_debug_orig)

    def _get_mem(self):
        # USS is the closest thing we have to "real" memory usage and it
        # should be less likely to produce false positives.
        mem = self._thisproc.memory_full_info()
        return getattr(mem, "uss", mem.rss)

    def _get_num_fds(self):
        if POSIX:
            return self._thisproc.num_fds()
        else:
            return self._thisproc.num_handles()

    def _log(self, msg):
        if self.verbose:
            print_color(msg, color="yellow", file=sys.stderr)

    def _check_fds(self, fun):
        """Makes sure num_fds() (POSIX) or num_handles() (Windows) does
        not increase after calling a function.  Used to discover forgotten
        close(2) and CloseHandle syscalls.
        """
        before = self._get_num_fds()
        self.call(fun)
        after = self._get_num_fds()
        diff = after - before
        if diff < 0:
            raise self.fail(
                "negative diff %r (gc probably collected a "
                "resource from a previous test)" % diff
            )
        if diff > 0:
            type_ = "fd" if POSIX else "handle"
            if diff > 1:
                type_ += "s"
            msg = "%s unclosed %s after calling %r" % (diff, type_, fun)
            raise self.fail(msg)

    def _call_ntimes(self, fun, times):
        """Get 2 distinct memory samples, before and after having
        called fun repeatedly, and return the memory difference.
        """
        gc.collect(generation=1)
        mem1 = self._get_mem()
        for x in range(times):
            ret = self.call(fun)
            del x, ret
        gc.collect(generation=1)
        mem2 = self._get_mem()
        self.assertEqual(gc.garbage, [])
        diff = mem2 - mem1  # can also be negative
        return diff

    def _check_mem(self, fun, times, retries, tolerance):
        messages = []
        prev_mem = 0
        increase = times
        for idx in range(1, retries + 1):
            mem = self._call_ntimes(fun, times)
            msg = "Run #%s: extra-mem=%s, per-call=%s, calls=%s" % (
                idx,
                bytes2human(mem),
                bytes2human(mem / times),
                times,
            )
            messages.append(msg)
            success = mem <= tolerance or mem <= prev_mem
            if success:
                if idx > 1:
                    self._log(msg)
                return
            else:
                if idx == 1:
                    print()  # NOQA
                self._log(msg)
                times += increase
                prev_mem = mem
        raise self.fail(". ".join(messages))

    # ---

    def call(self, fun):
        return fun()

    def execute(
        self, fun, times=None, warmup_times=None, retries=None, tolerance=None
    ):
        """Test a callable."""
        times = times if times is not None else self.times
        warmup_times = (
            warmup_times if warmup_times is not None else self.warmup_times
        )
        retries = retries if retries is not None else self.retries
        tolerance = tolerance if tolerance is not None else self.tolerance
        try:
            assert times >= 1, "times must be >= 1"
            assert warmup_times >= 0, "warmup_times must be >= 0"
            assert retries >= 0, "retries must be >= 0"
            assert tolerance >= 0, "tolerance must be >= 0"
        except AssertionError as err:
            raise ValueError(str(err))

        self._call_ntimes(fun, warmup_times)  # warm up
        self._check_fds(fun)
        self._check_mem(fun, times=times, retries=retries, tolerance=tolerance)

    def execute_w_exc(self, exc, fun, **kwargs):
        """Convenience method to test a callable while making sure it
        raises an exception on every call.
        """

        def call():
            self.assertRaises(exc, fun)

        self.execute(call, **kwargs)


def print_sysinfo():
    import collections
    import datetime
    import getpass
    import locale
    import pprint

    try:
        import pip
    except ImportError:
        pip = None
    try:
        import wheel
    except ImportError:
        wheel = None

    def print_section(section, info):
        print(  # NOQA
            "\n" + " {} ".format(section).center(70, "=") + "\n",
            file=sys.stderr,
        )
        if isinstance(info, str):
            print(info, file=sys.stderr)  # NOQA
        else:
            pprint.pprint(info)  # NOQA
        sys.stdout.flush()

    info = collections.OrderedDict()

    # OS
    if psutil.LINUX and which('lsb_release'):
        info['OS'] = sh('lsb_release -d -s')
    elif psutil.OSX:
        info['OS'] = 'Darwin %s' % platform.mac_ver()[0]
    elif psutil.WINDOWS:
        info['OS'] = "Windows " + ' '.join(map(str, platform.win32_ver()))
        if hasattr(platform, 'win32_edition'):
            info['OS'] += ", " + platform.win32_edition()
    else:
        info['OS'] = "%s %s" % (platform.system(), platform.version())
    info['arch'] = ', '.join(
        list(platform.architecture()) + [platform.machine()]
    )
    if psutil.POSIX:
        info['kernel'] = platform.uname()[2]

    # python
    info['python'] = ', '.join([
        platform.python_implementation(),
        platform.python_version(),
        platform.python_compiler(),
    ])
    info['pip'] = getattr(pip, '__version__', 'not installed')
    if wheel is not None:
        info['pip'] += " (wheel=%s)" % wheel.__version__

    # UNIX
    if psutil.POSIX:
        if which('gcc'):
            out = sh(['gcc', '--version'])
            info['gcc'] = str(out).split('\n')[0]
        else:
            info['gcc'] = 'not installed'
        s = platform.libc_ver()[1]
        if s:
            info['glibc'] = s

    # system
    info['fs-encoding'] = sys.getfilesystemencoding()
    lang = locale.getlocale()
    info['lang'] = '%s, %s' % (lang[0], lang[1])
    info['boot-time'] = datetime.datetime.fromtimestamp(
        psutil.boot_time()
    ).strftime("%Y-%m-%d %H:%M:%S")
    info['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info['user'] = getpass.getuser()
    info['home'] = os.path.expanduser("~")
    info['cwd'] = os.getcwd()
    info['pyexe'] = PYTHON_EXE
    info['hostname'] = platform.node()
    info['PID'] = os.getpid()

    # metrics
    info['cpus'] = psutil.cpu_count()
    info['loadavg'] = "%.1f%%, %.1f%%, %.1f%%" % (
        tuple([x / psutil.cpu_count() * 100 for x in psutil.getloadavg()])
    )
    mem = psutil.virtual_memory()
    info['memory'] = "%s%%, used=%s, total=%s" % (
        int(mem.percent),
        bytes2human(mem.used),
        bytes2human(mem.total),
    )
    swap = psutil.swap_memory()
    info['swap'] = "%s%%, used=%s, total=%s" % (
        int(swap.percent),
        bytes2human(swap.used),
        bytes2human(swap.total),
    )
    info['pids'] = len(psutil.pids())
    pinfo = psutil.Process().as_dict()
    pinfo.pop('memory_maps', None)
    info['proc'] = pinfo
    info['partitions'] = psutil.disk_partitions(all=True)

    print_section("psutil", info)

    if POSIX and which("mount"):
        print_section("mount", sh("mount"))

    if WINDOWS:
        print_section(
            "tasklist", subprocess.check_output(["tasklist"]).decode()
        )
    elif which("ps"):
        print_section(
            "ps aux", subprocess.check_output(["ps", "aux"]).decode()
        )

    # XXX
    if LINUX:
        with open("/proc/self/mountinfo") as f:
            data = f.read()
        print_section("mountinfo 1", data)
        print_section("mountinfo 2", repr(data))

    print("=" * 70, file=sys.stderr)  # NOQA
    sys.stdout.flush()


def is_win_secure_system_proc(pid):
    # see: https://github.com/giampaolo/psutil/issues/2338
    @memoize
    def get_procs():
        ret = {}
        out = sh("tasklist.exe /NH /FO csv")
        for line in out.splitlines()[1:]:
            bits = [x.replace('"', "") for x in line.split(",")]
            name, pid = bits[0], int(bits[1])
            ret[pid] = name
        return ret

    try:
        return get_procs()[pid] == "Secure System"
    except KeyError:
        return False


def _get_eligible_cpu():
    p = psutil.Process()
    if hasattr(p, "cpu_num"):
        return p.cpu_num()
    elif hasattr(p, "cpu_affinity"):
        return random.choice(p.cpu_affinity())
    return 0


class process_namespace:
    """A container that lists all Process class method names + some
    reasonable parameters to be called with. Utility methods (parent(),
    children(), ...) are excluded.

    >>> ns = process_namespace(psutil.Process())
    >>> for fun, name in ns.iter(ns.getters):
    ...    fun()
    """

    utils = [('cpu_percent', (), {}), ('memory_percent', (), {})]

    ignored = [
        ('as_dict', (), {}),
        ('children', (), {'recursive': True}),
        ('is_running', (), {}),
        ('memory_info_ex', (), {}),
        ('oneshot', (), {}),
        ('parent', (), {}),
        ('parents', (), {}),
        ('pid', (), {}),
        ('wait', (0,), {}),
    ]

    getters = [
        ('cmdline', (), {}),
        ('connections', (), {'kind': 'all'}),
        ('cpu_times', (), {}),
        ('create_time', (), {}),
        ('cwd', (), {}),
        ('exe', (), {}),
        ('memory_full_info', (), {}),
        ('memory_info', (), {}),
        ('name', (), {}),
        ('nice', (), {}),
        ('num_ctx_switches', (), {}),
        ('num_threads', (), {}),
        ('open_files', (), {}),
        ('ppid', (), {}),
        ('status', (), {}),
        ('threads', (), {}),
        ('username', (), {}),
    ]
    if POSIX:
        getters += [('uids', (), {})]
        getters += [('gids', (), {})]
        getters += [('terminal', (), {})]
        getters += [('num_fds', (), {})]
    if HAS_PROC_IO_COUNTERS:
        getters += [('io_counters', (), {})]
    if HAS_IONICE:
        getters += [('ionice', (), {})]
    if HAS_RLIMIT:
        getters += [('rlimit', (psutil.RLIMIT_NOFILE,), {})]
    if HAS_CPU_AFFINITY:
        getters += [('cpu_affinity', (), {})]
    if HAS_PROC_CPU_NUM:
        getters += [('cpu_num', (), {})]
    if HAS_ENVIRON:
        getters += [('environ', (), {})]
    if WINDOWS:
        getters += [('num_handles', (), {})]
    if HAS_MEMORY_MAPS:
        getters += [('memory_maps', (), {'grouped': False})]

    setters = []
    if POSIX:
        setters += [('nice', (0,), {})]
    else:
        setters += [('nice', (psutil.NORMAL_PRIORITY_CLASS,), {})]
    if HAS_RLIMIT:
        setters += [('rlimit', (psutil.RLIMIT_NOFILE, (1024, 4096)), {})]
    if HAS_IONICE:
        if LINUX:
            setters += [('ionice', (psutil.IOPRIO_CLASS_NONE, 0), {})]
        else:
            setters += [('ionice', (psutil.IOPRIO_NORMAL,), {})]
    if HAS_CPU_AFFINITY:
        setters += [('cpu_affinity', ([_get_eligible_cpu()],), {})]

    killers = [
        ('send_signal', (signal.SIGTERM,), {}),
        ('suspend', (), {}),
        ('resume', (), {}),
        ('terminate', (), {}),
        ('kill', (), {}),
    ]
    if WINDOWS:
        killers += [('send_signal', (signal.CTRL_C_EVENT,), {})]
        killers += [('send_signal', (signal.CTRL_BREAK_EVENT,), {})]

    all = utils + getters + setters + killers

    def __init__(self, proc):
        self._proc = proc

    def iter(self, ls, clear_cache=True):
        """Given a list of tuples yields a set of (fun, fun_name) tuples
        in random order.
        """
        ls = list(ls)
        random.shuffle(ls)
        for fun_name, args, kwds in ls:
            if clear_cache:
                self.clear_cache()
            fun = getattr(self._proc, fun_name)
            fun = functools.partial(fun, *args, **kwds)
            yield (fun, fun_name)

    def clear_cache(self):
        """Clear the cache of a Process instance."""
        self._proc._init(self._proc.pid, _ignore_nsp=True)

    @classmethod
    def test_class_coverage(cls, test_class, ls):
        """Given a TestCase instance and a list of tuples checks that
        the class defines the required test method names.
        """
        for fun_name, _, _ in ls:
            meth_name = 'test_' + fun_name
            if not hasattr(test_class, meth_name):
                msg = "%r class should define a '%s' method" % (
                    test_class.__class__.__name__,
                    meth_name,
                )
                raise AttributeError(msg)

    @classmethod
    def test(cls):
        this = set([x[0] for x in cls.all])
        ignored = set([x[0] for x in cls.ignored])
        klass = set([x for x in dir(psutil.Process) if x[0] != '_'])
        leftout = (this | ignored) ^ klass
        if leftout:
            raise ValueError("uncovered Process class names: %r" % leftout)


class system_namespace:
    """A container that lists all the module-level, system-related APIs.
    Utilities such as cpu_percent() are excluded. Usage:

    >>> ns = system_namespace
    >>> for fun, name in ns.iter(ns.getters):
    ...    fun()
    """

    getters = [
        ('boot_time', (), {}),
        ('cpu_count', (), {'logical': False}),
        ('cpu_count', (), {'logical': True}),
        ('cpu_stats', (), {}),
        ('cpu_times', (), {'percpu': False}),
        ('cpu_times', (), {'percpu': True}),
        ('disk_io_counters', (), {'perdisk': True}),
        ('disk_partitions', (), {'all': True}),
        ('disk_usage', (os.getcwd(),), {}),
        ('net_connections', (), {'kind': 'all'}),
        ('net_if_addrs', (), {}),
        ('net_if_stats', (), {}),
        ('net_io_counters', (), {'pernic': True}),
        ('pid_exists', (os.getpid(),), {}),
        ('pids', (), {}),
        ('swap_memory', (), {}),
        ('users', (), {}),
        ('virtual_memory', (), {}),
    ]
    if HAS_CPU_FREQ:
        getters += [('cpu_freq', (), {'percpu': True})]
    if HAS_GETLOADAVG:
        getters += [('getloadavg', (), {})]
    if HAS_SENSORS_TEMPERATURES:
        getters += [('sensors_temperatures', (), {})]
    if HAS_SENSORS_FANS:
        getters += [('sensors_fans', (), {})]
    if HAS_SENSORS_BATTERY:
        getters += [('sensors_battery', (), {})]
    if WINDOWS:
        getters += [('win_service_iter', (), {})]
        getters += [('win_service_get', ('alg',), {})]

    ignored = [
        ('process_iter', (), {}),
        ('wait_procs', ([psutil.Process()],), {}),
        ('cpu_percent', (), {}),
        ('cpu_times_percent', (), {}),
    ]

    all = getters

    @staticmethod
    def iter(ls):
        """Given a list of tuples yields a set of (fun, fun_name) tuples
        in random order.
        """
        ls = list(ls)
        random.shuffle(ls)
        for fun_name, args, kwds in ls:
            fun = getattr(psutil, fun_name)
            fun = functools.partial(fun, *args, **kwds)
            yield (fun, fun_name)

    test_class_coverage = process_namespace.test_class_coverage


def serialrun(klass):
    """A decorator to mark a TestCase class. When running parallel tests,
    class' unit tests will be run serially (1 process).
    """
    # assert issubclass(klass, unittest.TestCase), klass
    assert inspect.isclass(klass), klass
    klass._serialrun = True
    return klass


def retry_on_failure(retries=NO_RETRIES):
    """Decorator which runs a test function and retries N times before
    actually failing.
    """

    def logfun(exc):
        print("%r, retrying" % exc, file=sys.stderr)  # NOQA

    return retry(
        exception=AssertionError, timeout=None, retries=retries, logfun=logfun
    )


def skip_on_access_denied(only_if=None):
    """Decorator to Ignore AccessDenied exceptions."""

    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except psutil.AccessDenied:
                if only_if is not None:
                    if not only_if:
                        raise
                raise unittest.SkipTest("raises AccessDenied")

        return wrapper

    return decorator


def skip_on_not_implemented(only_if=None):
    """Decorator to Ignore NotImplementedError exceptions."""

    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except NotImplementedError:
                if only_if is not None:
                    if not only_if:
                        raise
                msg = (
                    "%r was skipped because it raised NotImplementedError"
                    % fun.__name__
                )
                raise unittest.SkipTest(msg)

        return wrapper

    return decorator


# ===================================================================
# --- network
# ===================================================================


# XXX: no longer used
def get_free_port(host='127.0.0.1'):
    """Return an unused TCP port. Subject to race conditions."""
    with contextlib.closing(socket.socket()) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def bind_socket(family=AF_INET, type=SOCK_STREAM, addr=None):
    """Binds a generic socket."""
    if addr is None and family in (AF_INET, AF_INET6):
        addr = ("", 0)
    sock = socket.socket(family, type)
    try:
        if os.name not in ('nt', 'cygwin'):
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr)
        if type == socket.SOCK_STREAM:
            sock.listen(5)
        return sock
    except Exception:
        sock.close()
        raise


def bind_unix_socket(name, type=socket.SOCK_STREAM):
    """Bind a UNIX socket."""
    assert psutil.POSIX
    assert not os.path.exists(name), name
    sock = socket.socket(socket.AF_UNIX, type)
    try:
        sock.bind(name)
        if type == socket.SOCK_STREAM:
            sock.listen(5)
    except Exception:
        sock.close()
        raise
    return sock


def tcp_socketpair(family, addr=("", 0)):
    """Build a pair of TCP sockets connected to each other.
    Return a (server, client) tuple.
    """
    with contextlib.closing(socket.socket(family, SOCK_STREAM)) as ll:
        ll.bind(addr)
        ll.listen(5)
        addr = ll.getsockname()
        c = socket.socket(family, SOCK_STREAM)
        try:
            c.connect(addr)
            caddr = c.getsockname()
            while True:
                a, addr = ll.accept()
                # check that we've got the correct client
                if addr == caddr:
                    return (a, c)
                a.close()
        except OSError:
            c.close()
            raise


def unix_socketpair(name):
    """Build a pair of UNIX sockets connected to each other through
    the same UNIX file name.
    Return a (server, client) tuple.
    """
    assert psutil.POSIX
    server = client = None
    try:
        server = bind_unix_socket(name, type=socket.SOCK_STREAM)
        server.setblocking(0)
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.setblocking(0)
        client.connect(name)
        # new = server.accept()
    except Exception:
        if server is not None:
            server.close()
        if client is not None:
            client.close()
        raise
    return (server, client)


@contextlib.contextmanager
def create_sockets():
    """Open as many socket families / types as possible."""
    socks = []
    fname1 = fname2 = None
    try:
        socks.append(bind_socket(socket.AF_INET, socket.SOCK_STREAM))
        socks.append(bind_socket(socket.AF_INET, socket.SOCK_DGRAM))
        if supports_ipv6():
            socks.append(bind_socket(socket.AF_INET6, socket.SOCK_STREAM))
            socks.append(bind_socket(socket.AF_INET6, socket.SOCK_DGRAM))
        if POSIX and HAS_CONNECTIONS_UNIX:
            fname1 = get_testfn()
            fname2 = get_testfn()
            s1, s2 = unix_socketpair(fname1)
            s3 = bind_unix_socket(fname2, type=socket.SOCK_DGRAM)
            for s in (s1, s2, s3):
                socks.append(s)
        yield socks
    finally:
        for s in socks:
            s.close()
        for fname in (fname1, fname2):
            if fname is not None:
                safe_rmpath(fname)


def check_net_address(addr, family):
    """Check a net address validity. Supported families are IPv4,
    IPv6 and MAC addresses.
    """
    import ipaddress  # python >= 3.3 / requires "pip install ipaddress"

    if enum and PY3 and not PYPY:
        assert isinstance(family, enum.IntEnum), family
    if family == socket.AF_INET:
        octs = [int(x) for x in addr.split('.')]
        assert len(octs) == 4, addr
        for num in octs:
            assert 0 <= num <= 255, addr
        if not PY3:
            addr = unicode(addr)
        ipaddress.IPv4Address(addr)
    elif family == socket.AF_INET6:
        assert isinstance(addr, str), addr
        if not PY3:
            addr = unicode(addr)
        ipaddress.IPv6Address(addr)
    elif family == psutil.AF_LINK:
        assert re.match(r'([a-fA-F0-9]{2}[:|\-]?){6}', addr) is not None, addr
    else:
        raise ValueError("unknown family %r" % family)


def check_connection_ntuple(conn):
    """Check validity of a connection namedtuple."""

    def check_ntuple(conn):
        has_pid = len(conn) == 7
        assert len(conn) in (6, 7), len(conn)
        assert conn[0] == conn.fd, conn.fd
        assert conn[1] == conn.family, conn.family
        assert conn[2] == conn.type, conn.type
        assert conn[3] == conn.laddr, conn.laddr
        assert conn[4] == conn.raddr, conn.raddr
        assert conn[5] == conn.status, conn.status
        if has_pid:
            assert conn[6] == conn.pid, conn.pid

    def check_family(conn):
        assert conn.family in (AF_INET, AF_INET6, AF_UNIX), conn.family
        if enum is not None:
            assert isinstance(conn.family, enum.IntEnum), conn
        else:
            assert isinstance(conn.family, int), conn
        if conn.family == AF_INET:
            # actually try to bind the local socket; ignore IPv6
            # sockets as their address might be represented as
            # an IPv4-mapped-address (e.g. "::127.0.0.1")
            # and that's rejected by bind()
            s = socket.socket(conn.family, conn.type)
            with contextlib.closing(s):
                try:
                    s.bind((conn.laddr[0], 0))
                except socket.error as err:
                    if err.errno != errno.EADDRNOTAVAIL:
                        raise
        elif conn.family == AF_UNIX:
            assert conn.status == psutil.CONN_NONE, conn.status

    def check_type(conn):
        # SOCK_SEQPACKET may happen in case of AF_UNIX socks
        SOCK_SEQPACKET = getattr(socket, "SOCK_SEQPACKET", object())
        assert conn.type in (
            socket.SOCK_STREAM,
            socket.SOCK_DGRAM,
            SOCK_SEQPACKET,
        ), conn.type
        if enum is not None:
            assert isinstance(conn.type, enum.IntEnum), conn
        else:
            assert isinstance(conn.type, int), conn
        if conn.type == socket.SOCK_DGRAM:
            assert conn.status == psutil.CONN_NONE, conn.status

    def check_addrs(conn):
        # check IP address and port sanity
        for addr in (conn.laddr, conn.raddr):
            if conn.family in (AF_INET, AF_INET6):
                assert isinstance(addr, tuple), type(addr)
                if not addr:
                    continue
                assert isinstance(addr.port, int), type(addr.port)
                assert 0 <= addr.port <= 65535, addr.port
                check_net_address(addr.ip, conn.family)
            elif conn.family == AF_UNIX:
                assert isinstance(addr, str), type(addr)

    def check_status(conn):
        assert isinstance(conn.status, str), conn.status
        valids = [
            getattr(psutil, x) for x in dir(psutil) if x.startswith('CONN_')
        ]
        assert conn.status in valids, conn.status
        if conn.family in (AF_INET, AF_INET6) and conn.type == SOCK_STREAM:
            assert conn.status != psutil.CONN_NONE, conn.status
        else:
            assert conn.status == psutil.CONN_NONE, conn.status

    check_ntuple(conn)
    check_family(conn)
    check_type(conn)
    check_addrs(conn)
    check_status(conn)


def filter_proc_connections(cons):
    """Our process may start with some open UNIX sockets which are not
    initialized by us, invalidating unit tests.
    """
    new = []
    for conn in cons:
        if POSIX and conn.family == socket.AF_UNIX:
            if MACOS and "/syslog" in conn.raddr:
                debug("skipping %s" % str(conn))
                continue
        new.append(conn)
    return new


# ===================================================================
# --- compatibility
# ===================================================================


def reload_module(module):
    """Backport of importlib.reload of Python 3.3+."""
    try:
        import importlib

        if not hasattr(importlib, 'reload'):  # python <=3.3
            raise ImportError
    except ImportError:
        import imp

        return imp.reload(module)
    else:
        return importlib.reload(module)


def import_module_by_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    if sys.version_info[0] < 3:
        import imp

        return imp.load_source(name, path)
    else:
        import importlib.util

        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


# ===================================================================
# --- others
# ===================================================================


def warn(msg):
    """Raise a warning msg."""
    warnings.warn(msg, UserWarning, stacklevel=2)


def is_namedtuple(x):
    """Check if object is an instance of namedtuple."""
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(isinstance(n, str) for n in f)


if POSIX:

    @contextlib.contextmanager
    def copyload_shared_lib(suffix=""):
        """Ctx manager which picks up a random shared CO lib used
        by this process, copies it in another location and loads it
        in memory via ctypes. Return the new absolutized path.
        """
        exe = 'pypy' if PYPY else 'python'
        ext = ".so"
        dst = get_testfn(suffix=suffix + ext)
        libs = [
            x.path
            for x in psutil.Process().memory_maps()
            if os.path.splitext(x.path)[1] == ext and exe in x.path.lower()
        ]
        src = random.choice(libs)
        shutil.copyfile(src, dst)
        try:
            ctypes.CDLL(dst)
            yield dst
        finally:
            safe_rmpath(dst)

else:

    @contextlib.contextmanager
    def copyload_shared_lib(suffix=""):
        """Ctx manager which picks up a random shared DLL lib used
        by this process, copies it in another location and loads it
        in memory via ctypes.
        Return the new absolutized, normcased path.
        """
        from ctypes import WinError
        from ctypes import wintypes

        ext = ".dll"
        dst = get_testfn(suffix=suffix + ext)
        libs = [
            x.path
            for x in psutil.Process().memory_maps()
            if x.path.lower().endswith(ext)
            and 'python' in os.path.basename(x.path).lower()
            and 'wow64' not in x.path.lower()
        ]
        if PYPY and not libs:
            libs = [
                x.path
                for x in psutil.Process().memory_maps()
                if 'pypy' in os.path.basename(x.path).lower()
            ]
        src = random.choice(libs)
        shutil.copyfile(src, dst)
        cfile = None
        try:
            cfile = ctypes.WinDLL(dst)
            yield dst
        finally:
            # Work around OverflowError:
            # - https://ci.appveyor.com/project/giampaolo/psutil/build/1207/
            #       job/o53330pbnri9bcw7
            # - http://bugs.python.org/issue30286
            # - http://stackoverflow.com/questions/23522055
            if cfile is not None:
                FreeLibrary = ctypes.windll.kernel32.FreeLibrary
                FreeLibrary.argtypes = [wintypes.HMODULE]
                ret = FreeLibrary(cfile._handle)
                if ret == 0:
                    WinError()
            safe_rmpath(dst)


# ===================================================================
# --- Exit funs (first is executed last)
# ===================================================================


# this is executed first
@atexit.register
def cleanup_test_procs():
    reap_children(recursive=True)


# atexit module does not execute exit functions in case of SIGTERM, which
# gets sent to test subprocesses, which is a problem if they import this
# module. With this it will. See:
# https://gmpy.dev/blog/2016/how-to-always-execute-exit-functions-in-python
if POSIX:
    signal.signal(signal.SIGTERM, lambda sig, _: sys.exit(sig))
