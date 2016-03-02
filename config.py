# CONFIGURATION FILE of Static HTML file browser for Dropbox

DROPBOX_BASE_URL = "https://dl.dropboxusercontent.com/u/31525733"

# this is a link to the icons directory
DROPBOX_LINK_TO_ICONS = "{base}/icons".format(base=DROPBOX_BASE_URL)

# here you can change the output of the program
SHOW_SERVER_INFO = True         # default: True
HIDE_HIDDEN_ENTRIES = True      # default: True
HIDE_INDEX_HTML_FILES = True    # default: True
HIDE_ICONS_FOLDER = False       # default: True
MONOSPACED_FONTS = True         # default: True
SERVER_INFO = "Apache/2.4.18 at dropbox.com Port 80"

#icons folder in your dropbox
DROPBOX_ICON_FOLDER = "/home/jabba/Dropbox/assets/static_html_icons"

# if you want to add more icons, you can do it here, but don't forget to
# add the gif file to the icons directory too.
extensions = {
    r'.txt' : 'text.gif',
    r'.png' : 'image2.gif',
    r'.jpg' : 'image2.gif',
    r'.jpeg' : 'image2.gif',
    r'.bmp' : 'image2.gif',
    r'.gif' : 'image2.gif',
    r'.doc' : 'doc.gif',
    r'.htm' : 'link.gif',
    r'.html' : 'link.gif',
    r'.mp3' : 'sound2.gif',
    r'.mp4' : 'sound2.gif',
    r'.flac' : 'sound2.gif',
    r'.wav' : 'sound2.gif',
    r'.wma' : 'sound2.gif',
    r'.midi' : 'sound2.gif',
    r'.py' : 'python.gif',
    r'.tex' : 'tex.gif',
    r'.tar' : 'tar.gif'
}
