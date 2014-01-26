#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2013 Aparajita Fishman
#
# License: MIT
#

"""This module exports the Flake8 plugin linter class."""

import os
from SublimeLinter.lint import persist, PythonLinter


class Flake8(PythonLinter):

    """Provides an interface to the flake8 python module/script."""

    syntax = 'python'
    cmd = ('flake8@python', '*', '-')
    version_args = '--version'
    version_re = r'^(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 2.1'
    _flake8_errors = (
        'F402',
        'F404',
        'F812',
        'F823',
        'F831',
        'F821',
        'F822',
        'E112',
        'E113',
        'E901',
        'E902',
        )
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>%s)|(?P<warning>([FEWCN]\d+))) '
        r'(?P<message>(?P<near>\'.+\') imported but unused|.*)'
    ) % '|'.join(_flake8_errors)
    multiline = True
    defaults = {
        '--select=,': '',
        '--ignore=,': '',
        '--builtins=,': '',
        '--max-line-length=': None,
        '--max-complexity=': -1
    }
    inline_settings = ('max-line-length', 'max-complexity')
    inline_overrides = ('select', 'ignore', 'builtins')
    module = 'flake8.engine'
    check_version = True

    # Internal
    report = None
    pyflakes_checker_module = None
    pyflakes_checker_class = None

    @classmethod
    def initialize(cls):
        """Initialize the class after plugin load."""

        super().initialize()

        if cls.module is None:
            return

        # This is tricky. Unfortunately pyflakes chooses to store
        # builtins in a class variable and union that with the builtins option
        # on every execution. This results in the builtins never being removed.
        # To fix that, we get a reference to the pyflakes.checker module and
        # pyflakes.checker.Checker class used by flake8. We can then reset
        # the Checker.builtIns class variable on each execution.

        try:
            from pkg_resources import iter_entry_points
        except ImportError:
            pass
        else:
            for entry in iter_entry_points('flake8.extension'):
                check = entry.load()

                if check.name == 'pyflakes':
                    from pyflakes import checker
                    cls.pyflakes_checker_module = checker
                    cls.pyflakes_checker_class = check
                    break

    def check(self, code, filename):
        """Run flake8 on code and return the output."""

        options = {
            'reporter': self.get_report()
        }

        type_map = {
            'select': [],
            'ignore': [],
            'builtins': '',
            'max-line-length': 0,
            'max-complexity': 0
        }

        self.build_options(options, type_map, transform=lambda s: s.replace('-', '_'))

        if persist.debug_mode():
            persist.printf('{} options: {}'.format(self.name, options))

        if self.pyflakes_checker_class is not None:
            # Reset the builtins to the initial value used by pyflakes.
            builtins = set(self.pyflakes_checker_module.builtin_vars).union(self.pyflakes_checker_module._MAGIC_GLOBALS)
            self.pyflakes_checker_class.builtIns = builtins

        linter = self.module.get_style_guide(**options)

        return linter.input_file(
            filename=os.path.basename(filename),
            lines=code.splitlines(keepends=True)
        )

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method because sometimes we capture near,
        and a column will always override near.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if near:
            col = None

        return match, line, col, error, warning, message, near

    def get_report(self):
        """Return the Report class for use by flake8."""
        if self.report is None:
            from pep8 import StandardReport

            class Report(StandardReport):

                """Provides a report in the form of a single multiline string, without printing."""

                def get_file_results(self):
                    """Collect and return the results for this file."""
                    self._deferred_print.sort()
                    results = ''

                    for line_number, offset, code, text, doc in self._deferred_print:
                        results += '{path}:{row}:{col}: {code} {text}\n'.format_map({
                            'path': self.filename,
                            'row': self.line_offset + line_number,
                            'col': offset + 1,
                            'code': code,
                            'text': text
                        })

                    return results

            self.__class__.report = Report

        return self.report
