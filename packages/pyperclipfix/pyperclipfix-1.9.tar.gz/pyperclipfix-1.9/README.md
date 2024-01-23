Pyperclipfix is is a cross-platform Python 3 module for copy and paste clipboard functions. It's just a fork of [pyperclip](https://github.com/asweigart/pyperclip) with several merged pull requests and some minor bugfixes/leftover code removals (including the Python 2 support, which was already broken in the official version).

Install on Windows: `pip install pyperclipfix`

Install on Linux/macOS: `pip3 install pyperclipfix`

Al Sweigart al@inventwithpython.com
BSD License

Example Usage
=============

    >>> import pyperclipfix
    >>> pyperclipfix.copy('The text to be copied to the clipboard.')
    >>> pyperclipfix.paste()
    'The text to be copied to the clipboard.'


Currently only handles plaintext.

On Windows, no additional modules are needed.

On Mac, this module makes use of the pyobjc module (if installed) or on the pbcopy and pbpaste commands, which should come with the os.

On Linux, on X11 this module makes use of the xclip or xsel commands, which should come with the os. Otherwise run "sudo apt-get install xclip" or "sudo apt-get install xsel" (Note: xsel does not always seem to work.)
On Wayland it makes use of wl-copy and wl-paste (which can be installed with "sudo apt-get install wl-clipboard"), or also gpaste on GNOME (preferred, can be installed with "sudo apt-get install gpaste").
Otherwise on Linux, you will need the qtpy or PyQT5 modules installed.

Support
-------

If you find this project helpful and would like to support its development, [consider donating to the original creator on Patreon](https://www.patreon.com/AlSweigart).
