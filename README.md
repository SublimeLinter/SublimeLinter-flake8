SublimeLinter-flake8
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8)

This linter plugin for [SublimeLinter](http://sublimelinter.readthedocs.org) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/).

## Installation
SublimeLinter must be installed in order to use this plugin. 

Please install via [Package Control](https://sublime.wbond.net/installation).

Before installing this plugin, you must ensure that `flake8` is installed on your system. To install `flake8`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html) (Python 3 requires pip3).

1. Install `flake8` (2.1 or later) by typing the following in a terminal:
   ```
   # For python2
   [sudo] pip install flake8

   # For python 3
   [sudo] pip3 install flake8
   ```

In order for `flake8` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

## Settings

Flake8 configuration can passed in the project settings, via the `args` key:

```
{
    "folders":
    [
        {
            "path": "."
        }
    ],
    "SublimeLinter":
    {
        "linters":
        {
            "flake8": {
                "disable": true,
                "args": [
                    "--max-line-length=120",
                    "--exclude=__pycache__,.direnv",
                ],
            }
        }
    }
}
```

- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

SublimeLinter-flake8 no longer refers to common flake8 configuration files.
