SublimeLinter-flake8
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/).


## Installation

SublimeLinter must be installed in order to use this plugin.

Install via [Package Control](https://packagecontrol.io) or `git clone` as usual.

Ensure that a `flake8` is actually installed somewhere on your system. Typically, `pip install flake8` on the command line will do that.

If you want to use a globally installed flake, make sure that it is available on the PATH. Before going any further, please read and follow the steps in ["Finding a linter executable"](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable) through "Validating your PATH" in the documentation.

Otherwise configure ["executable"](http://www.sublimelinter.com/en/latest/linter_settings.html#executable) or the ["python"](http://www.sublimelinter.com/en/latest/linter_settings.html#python) setting.

If you use pipenv, and you're working on a project with a Pipfile, everything should be automatic.


## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

Additional settings:

- `ignore_fixables` (default: `True`): filter warnings that Sublime can fix automatically (e.g. trailing white-space) on save.

SublimeLinter-flake8 works with common flake8 [configuration files](http://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations) and inline overrides. Note that by default the [working dir](http://www.sublimelinter.com/en/latest/linter_settings.html#working-dir) is set to an open folder attached to the current window of Sublime. Edit this setting if your config files are located in a subfolder, for example.

Use ["args"](http://www.sublimelinter.com/en/latest/linter_settings.html#args) if you want to pass additional command line arguments to `flake8`.

## Compatibility with `--per-file-ignores` and other flake8 plugins

SublimeLinter-flake8 is compatible with most flake8 plugins out of the box. However, plugins that rely on selecting or ignoring certain files based on filename may appear to be "broken" due to the way SublimeLinter runs during linting. This includes flake8's own `--per-file-ignores` [option](http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-per-file-ignores) introduced in 3.7.0, as well as plugins such as [flake8-aaa](https://github.com/jamescooke/flake8-aaa) and [flake8-pyi](https://github.com/ambv/flake8-pyi).

To make the source filename available to the `flake8` executable again, pass the `--stdin-display-name` option using SublimeLinter's ["args"](http://www.sublimelinter.com/en/latest/linter_settings.html#args) setting:

```
"args": ["--stdin-display-name", "${file:stdin}"]
```

Including the `:stdin` fallback ensures that files that have yet to be saved are still linted.
