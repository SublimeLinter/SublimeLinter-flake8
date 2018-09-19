from SublimeLinter.lint import PythonLinter
import re

CAPTURE_WS = re.compile(r'(\s+)')


class Flake8(PythonLinter):

    cmd = ('flake8', '--format', 'default', '${args}', '-')
    defaults = {
        'selector': 'source.python'
    }

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

    def reposition_match(self, line, col, m, virtual_view):
        """Reposition white-space errors."""
        code = m.error or m.warning

        if code in ('W291', 'W293'):
            txt = virtual_view.select_line(line).rstrip('\n')
            return (line, col, len(txt))

        if code.startswith('E1'):
            return (line, 0, col)

        if code.startswith('E2'):
            txt = virtual_view.select_line(line).rstrip('\n')
            match = CAPTURE_WS.match(txt[col:])
            if match is not None:
                length = len(match.group(1))
                return (line, col, col + length)

        if code == 'E302':
            return line - 1, 0, 1

        if code == 'E303':
            match = re.match(r'too many blank lines \((\d+)', m.message.strip())
            if match is not None:
                count = int(match.group(1))
                return (line - (count - 1), 0, count - 1)

        if code == 'E999':
            txt = virtual_view.select_line(line).rstrip('\n')
            last_col = len(txt)
            if col + 1 == last_col:
                return line, last_col, last_col

        if code == 'F401':
            # `near` contains the imported identifier.
            # Since, it is usual to spread imports on multiple lines, we
            # search MAX_LINES for `near` starting with the reported line.
            MAX_LINES = 10
            near = m.near
            pattern = re.compile(r'\b({})\b'.format(near))
            last_line = len(virtual_view._newlines) - 1

            for _line in range(line, min(line + MAX_LINES, last_line)):
                txt = virtual_view.select_line(_line)

                # Take the right most match, to count for
                # 'from util import util'
                matches = list(pattern.finditer(txt))
                if matches:
                    match = matches[-1]
                    return _line, match.start(1), match.end(1)

            # Fallback, but since `near` did not match, setting both to None
            # gives the desired result.
            m = m._replace(near=None)
            col = None

        return super().reposition_match(line, col, m, virtual_view)
