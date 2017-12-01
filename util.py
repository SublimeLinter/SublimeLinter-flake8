#
# util.py
#
# Copyright (c) 2015-2016 The SublimeLinter Community
#
# License: MIT
#

"""Utilities."""

from functools import lru_cache
import os
import subprocess


import sublime
from SublimeLinter.lint import util, persist


def _find_executables(executable):
    env = util.create_environment()

    for base in env.get('PATH', '').split(os.pathsep):
        path = os.path.join(os.path.expanduser(base), executable)

        # On Windows, if path does not have an extension, try .exe, .cmd, .bat
        if sublime.platform() == 'windows' and not os.path.splitext(path)[1]:
            for extension in ('.exe', '.cmd', '.bat'):
                path_ext = path + extension

                if util.can_exec(path_ext):
                    yield path_ext
        elif util.can_exec(path):
            yield path

    return None


@lru_cache(maxsize=None)
def find_executable(executable):
    """Return the full path to an executable searching PATH."""

    for path in _find_executables(executable):
        return path

    return None


def find_python_version(version):  # type: Str
    """Return python binaries on PATH matching a specific version."""

    requested_version = util.extract_major_minor_version(version)
    for python in _find_executables('python'):
        python_version = util.get_python_version(python)
        if util.version_fulfills_request(python_version, requested_version):
            yield python

    return None


@lru_cache(maxsize=None)
def find_script_by_python_version(script_name, version):
    """Return full path to a script, given just a python version."""

    # They can be multiple matching pythons. We try to find a python with
    # its complete environment, not just a symbolic link or so.
    for python in find_python_version(version):
        python_env = os.path.dirname(python)
        script_path = find_script_by_python_env(python_env, script_name)
        if script_path:
            return script_path

    return None


@lru_cache(maxsize=None)
def find_script_by_python_env(python_env_path, script):
    """Return full path to a script, given a python environment base dir."""

    posix = sublime.platform() in ('osx', 'linux')

    if posix:
        full_path = os.path.join(python_env_path, 'bin', script)
    else:
        full_path = os.path.join(python_env_path, 'Scripts', script + '.exe')

    persist.printf("trying {}".format(full_path))
    if os.path.exists(full_path):
        return full_path

    return None


def expand_variables(string):
    """Expand typical sublime variables in the given string."""

    window = sublime.active_window()
    env = window.extract_variables()
    return sublime.expand_variables(string, env)


def get_project_path():
    """Return the project_path using Sublime's window.project_data() API."""

    window = sublime.active_window()
    # window.project_data() is a relative new API.
    # I don't know what we can expect from 'folders' here. Can we just take
    # the first one, if any, and be happy?
    project_data = window.project_data() or {}
    folders = project_data.get('folders', [])
    if folders:
        return folders[0]['path']  # ?


def ask_pipenv(linter_name, chdir):
    """Ask pipenv for a virtual environment and maybe resolve the linter."""

    # Some pre-checks bc `pipenv` is super slow
    project_path = get_project_path()
    if not project_path:
        return

    pipfile = os.path.join(project_path, 'Pipfile')
    if not os.path.exists(pipfile):
        return

    # Defer the real work to another function we can cache.
    # ATTENTION: If the user has a Pipfile, but did not (yet) installed the
    # environment, we will cache a wrong result here.
    return _ask_pipenv(linter_name, chdir)


@lru_cache(maxsize=None)
def _ask_pipenv(linter_name, chdir):
    cmd = ['pipenv', '--venv']
    with util.cd(chdir):
        venv = _communicate(cmd).strip().split('\n')[-1]

    if not venv:
        return

    return find_script_by_python_env(venv, linter_name)


def _communicate(cmd):
    """Short wrapper around subprocess.check_output to eat all errors."""

    env = util.create_environment()
    info = None

    # On Windows, start process without a window
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

    try:
        return subprocess.check_output(
            cmd, env=env, startupinfo=info, universal_newlines=True
        )
    except Exception as err:
        persist.debug(
            "executing {} failed: reason: {}".format(cmd, str(err))
        )
        return ''


# re-export for convenience
find_python = util.find_python
can_exec = util.can_exec
