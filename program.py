#!/usr/bin/env python
# encoding: utf-8

# programmed by: Kiss Sándor Ádám
# kisssandoradam@gmail.com
# idea and a lots of help: Dr. Szathmáry László
# Project started on 2013. december 13 midnight
# University of Debrecen


"""
This script generates an index.html file to
every directory and subdirectory starting from
the containing directory. Every html file consist of
a table with the following rows:
icon file_name last_modification_time file_size

It is designed to look like the output of apache web server.
"""

# do not remove any of the following import lines!
import os
import sys
import re
import config
import requests
import datetime
import platform
from utils import sizeof_fmt
from time import gmtime, strftime
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree

# PATH is the location of the shared directory
PATH = ""
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def icon_path(name, is_directory=False, parent_link=False):
    """
    Returns the relative path of the icons folder.
    """

    if parent_link:
        return "back.gif"
    elif is_directory:
        return "folder.gif"
    else:   # not is_folder:
        for key, value in config.extensions.iteritems():
            match = re.search(key, name)
            # if we know the extension of the file
            if match is not None:
                return value
    
    # unknown filename extension
    return "unknown.gif"


class Data(object):
    """
    The object of this class contain information about one directory or
    about one file.
    """
    def __init__(self, name, current_directory, deep):
        if name == "Parent Directory":
            self.name = name
            self.url = "../index.html"
            self.icon = icon_path("", parent_link=True)
            self.type = "directory"
            self.date = ""
            self.size = "-"
            return

        self.pathtofile = current_directory + "/" + name
        # if it's a directory, then...
        if os.path.isdir(self.pathtofile):
            self.name = name + "/"
            self.url = name + "/index.html"
            self.icon = icon_path(name, is_directory=True)
            self.type = "directory"
            self.size = "-"
        else:
            self.name = name
            self.url = name
            self.icon = icon_path(name, is_directory=False)
            self.type = "file"
            self.size = sizeof_fmt(os.path.getsize(self.pathtofile))

        # converts date to human readable format
        # gmtime converts seconds since the Epoch to a time tuple expressing UTC
        self.date = strftime("%Y-%m-%d&nbsp;%H:%M", gmtime(60 * 60 + os.path.getmtime(self.pathtofile)))

        # this is required, beacuse we don't want absolute path from the real root
        # directory, just a relative path
        # Pl.: you will get "/" instead of "/shared/Dropbox/Public/"
        if current_directory == PATH:
            self.current_directory = "/"
        else:
            self.current_directory = current_directory[len(PATH):] + "/"        

    def __cmp__(self, other):
        """
        Compares the objects by their types and if the type is equal,
        then it compares them by their names.
        
        Ordering:
        First item: "Parent Directory"
        Second item - Nth item: Directories in lexicographic order
        Nth item - last item: Files in lexicographic order
        """
        if self.name == "Parent Directory" or other.name == "Parent Directory":
            return 0

        if self.type == other.type:
            if self.name < other.name:
                return -1
            elif self.name == other.name:
                return 0
            else:
                return 1
        elif self.type == "directory" and other.type == "file":
            return -1
        else:
            return 1



def get_directory_content(directory):
    """
    Returns a list with files and directories of the current directory.
    """

    content = os.listdir(directory)

    # symbolic links will not be added to the list!
    if config.SHOW_HIDDEN_ENTRIES and config.HIDE_INDEX_HTML_FILES:
        files = [ f for f in content if not os.path.islink(f) and f != "index.html" ]
    elif config.SHOW_HIDDEN_ENTRIES and not config.HIDE_INDEX_HTML_FILES:
        files = [ f for f in content if not os.path.islink(f) ]
    elif not config.SHOW_HIDDEN_ENTRIES and not config.HIDE_INDEX_HTML_FILES:
        files = [ f for f in content if not os.path.islink(f) and f[0] != "."]
    else:
        files = [ f for f in content if not os.path.islink(f) and f[0] != "." \
                    and f != "index.html" ]
    return files


def get_server_info():
    """
    generates the server info text, which is shown
    shown below the table if SHOW_SERVER_INFO is True
    """
    
    return "Apache/2.4.7 at dropbox.com Port 80"


processed_files = 0 # counts the processed files and directories
num_of_index_htmls = 1  # counts the generated index.html files
def create_index_html(current_directory = PATH, deep = 0):
    """
    Recursive function, that generates an index.html file to every
    directory and subdirectory.
    """

    # every directory and subdirectory will contain a file with fname
    fname = "index.html"

    # get the names of the files and directories in the current_directory
    files = get_directory_content(current_directory)

    li = [] # collects the files and directories with the required informations
   
     # the first element in the list should be always the Parent Directory link
    li.append( Data("Parent Directory", current_directory, deep) )

    # before every recursive call increase this value
    global num_of_index_htmls
    # iterate over the files list, which contaions the name of the files and dirs
    for filename in files:
        path_to_file = current_directory + "/" + filename
        # if the current file is a directory, we call the function recursively
        if os.path.isdir(path_to_file):
            num_of_index_htmls += 1
            create_index_html(path_to_file, deep + 1)

        li.append( Data(filename, current_directory, deep) )

    # see __cmp__ function of Data class
    li.sort()

    # increase the processed_files counter by the number of the
    # files and directories in the current directory
    global processed_files
    processed_files += len(li)-1    

    context = {
        'datas' : li,
        'SHOW_SERVER_INFO' : config.SHOW_SERVER_INFO,
        'server_info' : get_server_info(),
        'root' : PATH,
        'current_directory' : current_directory,
        'index_of' : current_directory[len(PATH)+1:],
        'font' : ( "monospace" if config.MONOSPACED_FONTS else "" ),
        'link_to_icons' : config.DROPBOX_LINK_TO_ICONS
    }

    with open(current_directory + "/" + fname, 'w') as f:
        html = render_template('template.html', context)
        f.write(html)


def mark_to_delete(current_directory):
    """
    Recursively creates a list with index.html files from the current_directory
    and returns the entire list. (These files can be deleted)
    """

    files = [ f for f in os.listdir(current_directory) if not os.path.islink(f) ]

    indexes = []
    for filename in files:
        path_to_file = current_directory + "/" + filename
        # if the current file is a directory, we call the function recursively
        if os.path.isdir(path_to_file):
            indexes += mark_to_delete(path_to_file)
        else:
            if filename == "index.html":
                indexes.append(path_to_file)

    return indexes


def clear_up(starting_directory=PATH):
    """
    This function is called when we run the program with "-del" parameter
    """

    print "Clearing up index.html files..."
    marked_to_delete = mark_to_delete(starting_directory)

    if len(marked_to_delete) == 0:
        print "There is nothing to remove. Exiting..."
        exit(0)

    print "The following files will be removed:"
    print "\n".join(marked_to_delete)
    print "You are going to remove {number} files.".format(number=len(marked_to_delete))
    
    # asking user to make sure what he wants to do!
    answer = raw_input("Are you sure you want to continue? You cannot undo this operation!(yes/no) ")
    if answer == "yes":
        for filename in marked_to_delete:
            os.unlink(filename)
        os.system("clear")
        print "You have removed {number} index.html files.".format(number=len(marked_to_delete))
    else:
        print "No files were removed!"
        exit(0)


def show_usage():
    sys.stdout.write("Before the first start you should edit config.py\n")
    sys.stdout.write("Usage of the program:\n")
    sys.stdout.write("python " + sys.argv[0])
    sys.stdout.write(" [-del] [location]\n")
    sys.stdout.write("\t[-del]\t\tdeletes every index.html files from the [location] directory\n")
    sys.stdout.write("\t[location]\tthis is the shared directory where index.html files will be generated\n")
    sys.stdout.write("Examples:\n")
    sys.stdout.write("\tpython " + sys.argv[0] + " ~/Dropbox/Public" "\n")


def main():
    global PATH
    print "Static HTML file browser for Dropbox"
    if len(sys.argv) != 1:
        # if the first command line argument is -install, then we copy icons folder to
        # the given directory, that can be found in config.py (see config.INSTALL_DIR).
        if sys.argv[1] == "-firstinstall":
            config.INSTALL_DIR = config.INSTALL_DIR + "/icons"
            print "Installing..."
            
            # before the installation everyone have to set up their own config.py
            try:
                answer = raw_input("Did you configured config.py? (yes/no) ")
            except (EOFError, KeyboardInterrupt):
                    print   # prints a new line
                    exit(1) # terminates the program

            if answer != "yes":
                print "Before running this program, you have to edit config.py with a text editor!"
                exit(0)

            # if the directory exists, then it will be deleted, and icons will be copied
            if os.path.isdir(config.INSTALL_DIR):
                try:
                    answer = raw_input("Would you like to overwrite the entire " + config.INSTALL_DIR + " directory? (yes/no) ")
                except (EOFError, KeyboardInterrupt):
                    print   # prints a new line
                    exit(1) # terminates the program
                if answer == "yes":
                    rmtree(config.INSTALL_DIR)
                    copytree("icons", config.INSTALL_DIR)
                else:
                    print "No change were made on the disk! Exiting..."
                    exit(0)

            # if everything is okey, then the program copies icons dir to Public folder
            elif os.path.isdir("icons"):
                copytree("icons", config.INSTALL_DIR)
                print "Installation successfully finished! Now check your " + config.INSTALL_DIR + " folder!"

            # can't find the icons folder in the same directory, where the program started
            else:
                sys.stderr.write("Cannot find local icons folder!\n")
                exit(1)
            exit(0)

        # the program tries to delete every index.html files recursively
        elif sys.argv[1] == "-del":
            try:
                PATH = sys.argv[2]
            except IndexError:
                show_usage()
                exit(1)
            clear_up(PATH)
            exit(0)
        
        # if the first cmd line argument is a directory, generate index.html files
        elif os.path.isdir(sys.argv[1]):
            PATH = sys.argv[1]
            create_index_html(PATH)
            print "Total processed files and directories: {n}".format(n=processed_files)
            print "Total index.html files generated: {n}".format(n=num_of_index_htmls)
            exit(0)

        # unknown cmd line argument was given
        else:
            sys.stderr.write("Unknown command line argument " + sys.argv[1] + "\n")
            show_usage()
            exit(1)

    # the program started without any cmd line arguments.
    else:
        show_usage()
        exit(0)

#############################################################################

if __name__ == "__main__":
    main()
