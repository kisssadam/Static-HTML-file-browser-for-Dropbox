# CONFIGURATION FILE of Static HTML file browser for Dropbox

# this is a link to the icons directory
DROPBOX_LINK_TO_ICONS = "https://dl.dropboxusercontent.com/u/31525733/icons"


# here you can change the output of the program
SHOW_SERVER_INFO = True         # default: True
HIDE_HIDDEN_ENTRIES = True      # default: True
HIDE_INDEX_HTML_FILES = True    # default: True
MONOSPACED_FONTS = True         # default: True
SERVER_INFO = "Apache/2.4.7 at dropbox.com Port 80"

#icons folder in your dropbox
DROPBOX_ICON_FOLDER = "/home/icsaba/Dropbox/icons/"


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
