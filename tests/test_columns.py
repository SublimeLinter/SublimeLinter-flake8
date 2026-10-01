import importlib
import unittest

import sublime
from SublimeLinter.lint.linter import VirtualView


Linter = importlib.import_module('SublimeLinter-flake8.linter').Flake8


class TestColumns(unittest.TestCase):
    def test_pyflakes_bytes_and_pycodestyle_characters_together(self):
        # Captured Flake8 7.4.1 output for the same source line.
        output = ("stdin:1:15: F821 undefined name 'missing_name'\n"
                  "stdin:1:9: E702 multiple statements on one line (semicolon)\n")
        self.assertDiagnostics(output, 's = "é😀"; missing_name\n', [(10, 'missing_name'), (8, ';')])

    def test_pycodestyle_operator_position_is_unchanged(self):
        output = 'stdin:1:2: E225 missing whitespace around operator'
        self.assertDiagnostics(output, 's="é😀"\n', [(1, '=')])

    def test_trailing_whitespace_repositioning_is_preserved(self):
        self.assertDiagnostics('stdin:1:9: W291 trailing whitespace', 's = "é😀"   \n', [(8, '   ')])

    def test_unused_import_repositioning_is_preserved(self):
        output = "stdin:1:1: F401 'os.path' imported but unused"
        self.assertDiagnostics(output, 'from os import path\n', [(15, 'path')])

    def test_ascii_pyflakes_position_is_unchanged(self):
        output = "stdin:1:1: F821 undefined name 'missing_name'"
        self.assertDiagnostics(output, 'missing_name\n', [(0, 'missing_name')])

    def assertDiagnostics(self, output, source, expected):
        linter = Linter(sublime.View(0), {})
        matches = list(linter.find_errors(output))
        self.assertEqual(len(matches), len(expected))
        for match, (col, text) in zip(matches, expected):
            before = dict(match)
            error = linter.process_match(match, VirtualView(source))
            self.assertIsNotNone(error)
            self.assertEqual(match, before)
            self.assertEqual({k: error[k] for k in ('line', 'start', 'region', 'offending_text')}, {
                'line': 0, 'start': col, 'region': sublime.Region(col, col + len(text)),
                'offending_text': text,
            })
