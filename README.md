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
* Linux (or Windows, but i can't give you any help how to use this program on Windows)
* Python 2.7.6 interpreter (only this was tested while i was developing the application)
* The following modules must be installed:
  + requests
  + jinja2

Installation
------------
1. Before you start the program, please edit the config.py file with your favourite text editor (LibreOffice and other Office tools are not text editors, they are word processors, so please do not use them!)
The set up takes about 30 seconds if you read the comments in config.py
2. Now start the program without any command line arguments! There will be a short info about it.
3. Use "program.py --install location" command, and it will copy "icons" directory to a specified directory (this can be set up in the config.py)
4. Start the program with a location command line argument, that is the path of the Public folder of your Dropbox directory. Example: python program.py ~/Dropbox/Public
5. Try it out! Share the link of the index.html file which is in the root directory of Dropbox/Public folder. With a webbrowser you can open it or even share it on the internet.

Contributors
----------------

[Jabba Laci](https://github.com/jabbalaci)


Things to do
------------
Implementing these features can tike a while beacuse i'm studying.
* -v --verbose command line arguments for verbose output
* Make it possible to generate a report.html file that contains the entire output of the program
* Add new command line arguments: --silent or --quiet to make no output (should work like: ./program > /dev/null)
* Make a linux service that runs in the background and scans the Public folder for changes. When it's content is changed it will automatically regenerate index.html files.
* Make it possible to skip files in the public folder and this feature can be reached by using an other index file for htmls. For example: index.html contains every files, but index2.html contains only those files that are not on the blacklist.
* Graphical user interfice in Qt or Java SE 7 to configure the program
