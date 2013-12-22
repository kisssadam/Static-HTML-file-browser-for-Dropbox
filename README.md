Static-HTML-file-browser-for-Dropbox
====================================

About the program
------------
This program can generate index.html files to every directory in your Dropbox/Public folder (or any other shared folder) and makes it possible to navigate online between these directories when it looks like an output of apache web server.

System Requirements
-------------------
* Dropbox account. If you don't have one, you can register:
  + By the way this program is free, but if you want to help me to get more free space on Dropbox, please use the following link to create a new Dropbox account: https://db.tt/3La8trR
  + If you don't want to help me to get more free space on Dropbox, please use this link to create a new Dropbox account: https://www.dropbox.com/
* Linux (or Windows, but i can't give you any help how to use this program on Windows)
* Python 2.7.6 interpreter (only this was tested while i was developing the application)
* The following modules must be installed:
  + requests
  + jinja2

Installation
------------
1. Before you start the program, please edit the config.py file with your favourite text editor (LibreOffice and other Office tools are not text editors, they are word processors, so please do not use them!)
The set up takes about 2 minutes if you read the comments in config.py
2. Now start the program without any command line arguments! There will be a short info about it.
3. Start program.py with -install command line argument, and it will copy "icons" directory to a specified directory (this can be set up in the config.py)
4. Start the program with a location command line argument, that is the path of the Public folder of your Dropbox directory. Example: python program.py ~/Dropbox/Public
5. Try it out! Share the link of the index.html file which is in the root directory of Dropbox/Public folder. With a webbrowser you can open it or even share it on the internet.

