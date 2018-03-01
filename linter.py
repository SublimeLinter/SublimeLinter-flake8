from SublimeLinter.lint import PythonLinter


class Flake8(PythonLinter):

    syntax = ('python', 'python3')
    cmd = ('flake8', '--format', 'default', '${args}', '-')

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
