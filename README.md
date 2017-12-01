SublimeLinter-flake8
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-flake8)

This linter plugin for [SublimeLinter](http://sublimelinter.readthedocs.org) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/). It will be used with files that have the “Python” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here](http://sublimelinter.readthedocs.org/en/latest/installation.html).

### Linter installation
Before installing this plugin, you must ensure that `flake8` is installed on your system. To install `flake8`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html) (Python 3 requires pip3).

1. Install `flake8` by typing the following in a terminal:
   ```
   # For python2
   [sudo] pip install flake8

   # For python 3
   [sudo] pip3 install flake8
   ```

**Note:** This plugin requires `flake8` 2.1 or later.

### Linter configuration
In order for `flake8` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

Once `flake8` is installed and configured, you can proceed to install the SublimeLinter-flake8 plugin if it is not yet installed.

### Plugin installation
Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `flake8`. Among the entries you should see `SublimeLinter-flake8`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings](http://sublimelinter.readthedocs.org/en/latest/settings.html). For information on generic linter settings, please see [Linter Settings](http://sublimelinter.readthedocs.org/en/latest/linter_settings.html).

In addition to the standard SublimeLinter settings, SublimeLinter-flake8 provides its own settings. Those marked as “Inline Setting” or “Inline Override” may also be [used inline](http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings).

|Setting|Description|Inline Setting|Inline Override|
|:------|:----------|:------------:|:-------------:|
|@python|A meta setting that indicates the [python version](http://sublimelinter.readthedocs.org/en/latest/meta_settings.html#python) of your source files. Use this inline or at the global level, not within the linter’s settings.|&#10003;| |
|select|A comma-separated list of error codes to select, overrides ignore| |&#10003;|
|ignore|A comma-separated list of error codes to ignore| |&#10003;|
|builtins|A comma-separated string with external names that should be considered defined (e.g. "foo,bar")| |&#10003;|
|max-line-length|The maximum allowed line length. `null` uses the PEP8 default of 79.|&#10003;| |
|max-complexity|The maximum allowed code complexity. -1 allows unlimited complexity.|&#10003;| |
|show-code|Displays the flake8 error code in the message, `False` by default.|&#10003;| |
|config|Absolute path to any ini-style config file. `None` by default uses settings.| |&#10003;|

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.

Thank you for helping out!
