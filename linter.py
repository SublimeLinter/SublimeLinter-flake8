import logging
from SublimeLinter.lint import PythonLinter
import re


logger = logging.getLogger('SublimeLinter.plugins.flake8')


CAPTURE_WS = re.compile(r'(\s+)')
CAPTURE_IMPORT_ID = re.compile(r'^\'(?:.*\.)?(.+)\'')
CAPTURE_F403_HINT = re.compile(r"'(.*)?'")


class Flake8(PythonLinter):

    cmd = ('flake8', '--format', 'default', '${args}', '-')
    defaults = {
        'selector': 'source.python',

        # Ignore codes Sublime can auto-fix
        'ignore_fixables': True
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
        r'(?P<warning>\w+\d+)) '
        r'(?P<message>.*)'
    )
    multiline = True

    def on_stderr(self, stderr):
        # For python 3.7 we actually have the case that flake yields
        # FutureWarnings. We just eat those as they're irrelevant here. Note
        # that we try to eat the subsequent line as well which usually contains
        # the culprit source line.
        stderr = re.sub(r'^.+FutureWarning.+\n(.*\n?)?', '', stderr, re.M)
        stderr = re.sub(r'^.+DeprecationWarning.+\n(.*\n?)?', '', stderr, re.M)

        if stderr:
            self.notify_failure()
            logger.error(stderr)

    def parse_output(self, proc, virtual_view):
        settings = self.get_view_settings()
        errors = super().parse_output(proc, virtual_view)

        if not settings.get('ignore_fixables', True):
            return errors

        trims_ws = self.view.settings().get('trim_trailing_white_space_on_save')
        ensures_newline = self.view.settings().get('ensure_newline_at_eof_on_save')

        if not (trims_ws or ensures_newline):
            return errors

        filtered_errors = []
        for error in errors:
            code = error['code']

            if ensures_newline and code == 'W292':
                continue

            if trims_ws and code in ('W291', 'W293'):
                continue

            if trims_ws and code == 'W391':
                # Fixable if one WS line is at EOF, except the view only has
                # one line.
                lines = len(virtual_view._newlines) - 1
                if (
                    virtual_view.select_line(lines - 1).strip() == ''
                    and (
                        lines < 2
                        or virtual_view.select_line(lines - 2).strip() != ''
                    )
                ):
                    continue

            filtered_errors.append(error)

        return filtered_errors

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
            # Typical message from flake is "'x.y.z' imported but unused"
            # The import_id will be 'z' in that case.
            # Since, it is usual to spread imports on multiple lines, we
            # search MAX_LINES for `import_id` starting with the reported line.
            MAX_LINES = 10
            match = CAPTURE_IMPORT_ID.search(m.message)
            if match:
                import_id = match.group(1)

                if import_id == '*':
                    pattern = re.compile(r'(\*)')
                else:
                    pattern = re.compile(r'\b({})\b'.format(re.escape(import_id)))

                last_line = len(virtual_view._newlines) - 1
                for _line in range(line, min(line + MAX_LINES, last_line)):
                    txt = virtual_view.select_line(_line)

                    # Take the right most match, to count for
                    # 'from util import util'
                    matches = list(pattern.finditer(txt))
                    if matches:
                        match = matches[-1]
                        return _line, match.start(1), match.end(1)

            # Fallback, and mark the line.
            col = None

        if code == 'F403':
            txt = virtual_view.select_line(line).rstrip('\n')
            match = CAPTURE_F403_HINT.search(m.message)
            if match:
                hint = match.group(1)
                start = txt.find(hint)
                if start >= 0:
                    return line, start + len(hint) - 1, start + len(hint)

        return super().reposition_match(line, col, m, virtual_view)
