from functools import lru_cache
import os

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
    for path in _find_executables(executable):
        return path

    return None


def find_python_version(version):  # type: Str
    requested_version = util.extract_major_minor_version(version)
    for python in _find_executables('python'):
        python_version = util.get_python_version(python)
        if util.version_fulfills_request(python_version, requested_version):
            yield python

    return None


@lru_cache(maxsize=None)
def find_script_by_python_version(script_name, version):
    """
    Given a version string for python and a script name, try to return a
    full path to such a script if any.
    """

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
    """
    Return full path to a script installed in a python environment.

    `python_env_path` is the base path of a python installation or virtual
    environment.
    """
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
    window = sublime.active_window()
    env = window.extract_variables()
    return sublime.expand_variables(string, env)


# re-export for convenience
find_python = util.find_python
can_exec = util.can_exec
