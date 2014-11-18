Static HTML file browser for Dropbox
====================================

Screenshot about output
------------------
![screenshot not available](https://raw.github.com/kisssandoradam/Static-HTML-file-browser-for-Dropbox/master/screenshot.png)

About the program
------------
This program can generate html files to every directory in your Dropbox/Public folder (or any other shared folder) and makes it possible to navigate online between these directories when it looks like an output of apache web server.

Requirements
-------------------
* Dropbox account. If you don't have one, you can register here: https://db.tt/3La8trR
* Linux (or Windows, but I can't give you any help how to use this program under Windows)
* Python 2.7 interpreter (only this was tested while i was developing the application, newer than 3.0 interpreters may not work)
* The following modules must be installed:
  + jinja2

Installation
------------
1. Before starting the program, please edit the config.py with your favourite text editor. Setting up takes less than 30 seconds if you read the comments in config.py
2. Now start program.py with -h or --help command line argument. There will be a short info about it.
    ```python program.py --help```
3. Use "program.py --install location" command, and it will copy "icons" directory to the specified directory.
    ```python program.py ~/Dropbox/Public/```
4. Start the program with a location command line argument, which is the path of the Public folder of your Dropbox directory.
    ```python program.py ~/Dropbox/Public/```
5. Try it out! Share the link of the index.html file which is in the root directory of Dropbox/Public folder. You can open it with a webbrowser or you can share it on the internet.

Contributors
----------------

[Jabba Laci](https://github.com/jabbalaci)
