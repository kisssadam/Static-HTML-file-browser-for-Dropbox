# CONFIGURATION FILE of Static HTML file browser for Dropbox

# SET UP INSTALLATION DIRECTORY (this should be absolute path!)
# this is the shared directory of your Dropbox folder
INSTALL_DIR = "/home/adam/Dropbox/Public"

# this is a link to the icons directory
DROPBOX_LINK_TO_ICONS = "https://dl.dropboxusercontent.com/u/31525733/icons"


# here you can change the output of the program
SHOW_SERVER_INFO = True         # default: True
SHOW_HIDDEN_ENTRIES = False     # default: False
HIDE_INDEX_HTML_FILES = True    # default: True
MONOSPACED_FONTS = True         # default: True

# if you want to add more icons, you can do it here, but don't forget to
# add the gif file to the icons directory too.
extensions = {
    r'.txt' : 'text.gif',
    r'.png' : 'png.gif',
    r'.doc' : 'doc.gif',
    r'.htm' : 'link.gif',
    r'.mp3' : 'sound2.gif',
    r'.mp4' : 'sound2.gif',
    r'.flac' : 'sound2.gif',
    r'.wav' : 'sound2.gif',
    r'.wma' : 'sound2.gif',
    r'.midi' : 'sound2.gif',
    r'.py' : 'python.gif'
}
