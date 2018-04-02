SublimeLinter-flake8
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/).


## Installation

SublimeLinter must be installed in order to use this plugin. 

Please install via [Package Control](https://packagecontrol.io).

Before installing this plugin, ensure that `flake8` is installed on your system.
To install `flake8`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html) (Python 3 requires pip3).

1. Install `flake8` (2.1 or later) by typing the following in a terminal:
   ```
   # For python2
   [sudo] pip install flake8

   # For python 3
   [sudo] pip3 install flake8
   ```

Please make sure that the path to `flake8` is available to SublimeLinter. Before going any further, please read and follow the steps in ["Finding a linter executable"](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable) through "Validating your PATH" in the documentation.


## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

SublimeLinter-flake8 works with common flake8 [configuration files](http://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations) and inline overrides.
