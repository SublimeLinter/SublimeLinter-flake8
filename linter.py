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

from SublimeLinter.lint import PythonLinter


class Flake8(PythonLinter):
    """Provides an interface to the flake8 python module/script."""

    syntax = ('python', 'python3')
    cmd = ('flake8@python', '*', '-')
    version_args = '--version'
    version_re = r'^(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 2.2.2'
    check_version = True

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
        '--max-line-length=': None,
        '--max-complexity=': -1,
        '--jobs=': '1',
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

    def build_cmd(self, cmd=None):
        """Return a tuple with the command line to execute."""

        executable = self.get_view_settings().get('executable', None)
        if executable:
            args = (cmd or self.cmd)[1:]
            cmd = (executable, ) + args
            return self.insert_args(cmd)
        else:
            return super().build_cmd(cmd)
