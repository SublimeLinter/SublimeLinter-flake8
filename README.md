SublimeLinter-flake8
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/). It will be used with files that have the “Python” syntax.

## SublimeLinter 4 beta

We're making big improvements to how SublimeLinter works. You can read more about it [here](https://github.com/SublimeLinter/SublimeLinter3/blob/next/messages/4.0.0-rc.1.txt).

Participate in the beta right now by editing your Package Control preferences and adding SublimeLinter and SublimeLinter-flake8 to the "install_prereleases" key:  
```json
"install_prereleases":
[
  "SublimeLinter",
  "SublimeLinter-flake8"
]
```


## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before installing this plugin, you must ensure that `flake8` (2.1 or later) is installed on your system. To install `flake8`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html) (Python 3 requires pip3).

1. Install `flake8` by typing the following in a terminal:
   ```
   # For python2
   [sudo] pip install flake8

   # For python 3
   [sudo] pip3 install flake8
   ```


In order for `flake8` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).


## Settings
- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

Additional settings for SublimeLinter-flake8:

|Setting|Description|
|:------|:----------|
|@python|A meta setting that indicates the [python version](http://sublimelinter.readthedocs.org/en/latest/meta_settings.html#python) of your source files. Use this inline or at the global level, not within the linter’s settings.|
|builtins|A comma-separated string with external names that should be considered defined (e.g. "foo,bar")|
|show-code|Displays the flake8 error code in the message, `False` by default.|

Please use [flake8 configuration](http://flake8.pycqa.org/en/latest/user/configuration.html) (via config files or inline comments).
