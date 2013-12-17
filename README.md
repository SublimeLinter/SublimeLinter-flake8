SublimeLinter-flake8
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) provides an interface to [flake8](http://flake8.readthedocs.org/en/latest/). It will be used with files that have the “Python” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Installation).

### Linter installation
Before installing this plugin, you must ensure that `flake8` is installed on your system. To install `flake8`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html). If you plan to code in Python 3, you will need to install `pip` for Python 3 as well.

1. Install `flake8` by typing the following in a terminal, replacing ‘x’ with the minor version installed on your system:
   ```
   # For python 2.x
   [sudo] pip-2.x install flake8

   # For python 3.x
   [sudo] pip-3.x install flake8
   ```

Once flake8 is installed, you can proceed to install the SublimeLinter-flake8 plugin if it is not yet installed.

### Plugin installation
Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `flake8`. Among the entries you should see `SublimeLinter-flake8`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Settings). For information on generic linter settings, please see [Linter Settings](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Linter-Settings).

In addition to the standard SublimeLinter settings, SublimeLinter-flake8 provides its own settings. Those marked as “Inline Setting” or “Inline Override” may also be [used inline](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Settings#inline-settings).

|Setting|Description|Inline Setting|Inline Override|
|:------|:----------|:------------:|:-------------:|
|ignore|A comma-separated list of error codes to ignore| |&#10003;|
|select|A comma-separated list of error codes to select, overrides ignore| |&#10003;|
|max-line-length|The maximum allowed line length. `null` uses the PEP8 default of 79.|&#10003;| |
|max-complexity|The maximum allowed code complexity. -1 allows unlimited complexity.|&#10003;| |

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
