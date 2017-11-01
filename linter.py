#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2013-2014 Aparajita Fishman
# Copyright (c) 2015-2016 The SublimeLinter Community
#
# License: MIT
#

"""This module exports the Flake8 plugin linter class."""

from functools import lru_cache

from SublimeLinter.lint import Linter, persist
from . import util


class PythonLinter(Linter):
    """New base for the Flake8 linter.

    Supposed to work for other python linters as well. But not yet.
    """

    @classmethod
    @lru_cache(maxsize=None)
    def can_lint(cls, syntax):
        """Determine optimistically if the linter can handle the provided syntax."""
        can = False
        syntax = syntax.lower()

        if cls.syntax:
            if isinstance(cls.syntax, (tuple, list)):
                can = syntax in cls.syntax
            elif cls.syntax == '*':
                can = True
            elif isinstance(cls.syntax, str):
                can = syntax == cls.syntax
            else:
                can = cls.syntax.match(syntax) is not None

        return can

    def context_sensitive_executable_path(self, cmd):
        """Try to find an executable for a given cmd."""

        settings = self.get_view_settings()

        # If the user explicitly set an executable, it takes precedence.
        # We expand environment variables. E.g. a user could have a project
        # structure where a virtual environment is always located within
        # the project structure. She could then simply specify
        # `${project_path}/venv/bin/flake8`. Note that setting `@python`
        # to a path will have a similar effect.
        executable = settings.get('executable', '')
        if executable:
            executable = util.expand_variables(executable)

            persist.printf(
                "{}: wanted executable is '{}'".format(self.name, executable)
            )

            if util.can_exec(executable):
                return True, executable

            persist.printf(
                "ERROR: {} deactivated, cannot locate '{}' "
                .format(self.name, executable)
            )
            # no fallback, the user specified something, so we err
            return True, None

        # `@python` can be number or a string. If it is a string it should
        # point to a python environment, NOT a python binary.
        # We expand environment variables. E.g. a user could have a project
        # structure where virtual envs are located always like such
        # `some/where/venvs/${project_base_name}` or she has the venv
        # contained in the project dir `${project_path}/venv`. She then
        # could edit the global settings once and can be sure that always the
        # right linter installed in the virtual environment gets executed.
        python = settings.get('@python', None)
        if isinstance(python, str):
            python = util.expand_variables(python)

        persist.printf(
            "{}: wanted @python is '{}'".format(self.name, python)
        )

        cmd_name = cmd[0] if isinstance(cmd, (list, tuple)) else cmd

        if python:
            if isinstance(python, str):
                executable = util.find_script_by_python_env(
                    python, cmd_name
                )
                if not executable:
                    persist.printf(
                        "WARNING: {} deactivated, cannot locate '{}' "
                        "for given @python '{}'"
                        .format(self.name, cmd_name, python)
                    )
                    # Do not fallback, user specified something we didn't find
                    return True, None

                return True, executable

            else:
                executable = util.find_script_by_python_version(
                    cmd_name, str(python)
                )

                # If we didn't find anything useful, use the legacy
                # code from SublimeLinter for resolving that version.
                if executable is None:
                    persist.printf(
                        "{}: Still trying to resolve {}, now trying "
                        "SublimeLinter's legacy code."
                        .format(self.name, python)
                    )
                    _, executable, *_ = util.find_python(
                        str(python), cmd_name
                    )

                if executable is None:
                    persist.printf(
                        "WARNING: {} deactivated, cannot locate '{}' "
                        "for given @python '{}'"
                        .format(self.name, cmd_name, python)
                    )
                    return True, None

                persist.printf(
                    "{}: Using {} for given @python '{}'"
                    .format(self.name, executable, python)
                )
                return True, executable

        # If we're here the user didn't specify anything. This is the default
        # experience. So we kick in some 'magic'
        chdir = self.get_chdir(settings)
        executable = util.ask_pipenv(cmd[0], chdir)
        if executable:
            persist.printf(
                "{}: Using {} according to 'pipenv'"
                .format(self.name, executable)
            )
            return True, executable

        # Should we try a `pyenv which` as well? Problem: I don't have it,
        # it's MacOS only.

        persist.printf(
            "{}: trying to use globally installed {}"
            .format(self.name, cmd_name)
        )
        # fallback, similiar to a which(cmd)
        executable = util.find_executable(cmd_name)
        if executable is None:
            persist.printf(
                "WARNING: cannot locate '{}'. Fill in the '@python' or "
                "'executable' setting."
                .format(self.name)
            )
        return True, executable


class Flake8(PythonLinter):
    """Provides an interface to the flake8 python module/script."""

    syntax = ('python', 'python3')
    cmd = ('flake8', '*', '-')  # do not specify `@python` bc we do our own

    # The following regex marks these pyflakes and pep8 codes as errors.
    # All other codes are marked as warnings.
    #
    # Pyflake Errors:
    #  - F402 import module from line N shadowed by loop variable
    #  - F404 future import(s) name after other statements
    #  - F812 list comprehension redefines name from line N
    #  - F823 local variable name ... referenced before assignment
    #  - F831 duplicate argument name in function definition
    #  - F821 undefined name name
    #  - F822 undefined name name in __all__
    #
    # Pep8 Errors:
    #  - E112 expected an indented block
    #  - E113 unexpected indentation
    #  - E901 SyntaxError or IndentationError
    #  - E902 IOError
    #  - E999 SyntaxError

    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>(?:F(?:40[24]|8(?:12|2[123]|31))|E(?:11[23]|90[12]|999)))|'
        r'(?P<warning>\w\d+)) '
        r'(?P<message>\'(.*\.)?(?P<near>.+)\' imported but unused|.*)'
    )
    multiline = True
    defaults = {
        '--select=,': '',
        '--ignore=,': '',
        '--builtins=,': '',
        '--max-line-length=': '',
        '--max-complexity=': '',
        '--jobs=': '',
        'show-code': False,
        'executable': ''
    }
    inline_settings = ('max-line-length', 'max-complexity')
    inline_overrides = ('select', 'ignore', 'builtins')

    # ST will not show error marks in whitespace errors, so bump the column by one
    # e.g. `E203 whitespace before ':'`
    increment_col = ('E203',)

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method because sometimes we capture near,
        and a column will always override near.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if near:
            col = None

        if col and any(c in self.increment_col for c in (error, warning)):
            col += 1

        if self.get_view_settings().get('show-code'):
            message = ' '.join([error or warning or '', message])
        return match, line, col, error, warning, message, near
