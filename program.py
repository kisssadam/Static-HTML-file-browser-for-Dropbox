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
import re
import config
import requests
import datetime
import platform
from utils import sizeof_fmt, install, cleanup, fix_location
from time import gmtime, strftime
from jinja2 import Environment, FileSystemLoader
from shutil import copytree, rmtree
import argparse

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

        #self.pathtofile = current_directory + "/" + name
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

    def __str__(self):
        """Returns the absolute filepath to the file including the filename"""
        return fix_location(self.pathtofile)


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
    below the table if SHOW_SERVER_INFO is True
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

    filelist = [] # collects the files and directories with the required informations
   
     # the first element in the list should be always the Parent Directory link
    filelist.append( Data("Parent Directory", current_directory, deep) )

    # before every recursive call increase this value
    global num_of_index_htmls
    # iterate over the files list, which contaions the name of the files and dirs
    for filename in files:
        path_to_file = current_directory + "/" + filename
        # if the current file is a directory, we call the function recursively
        try:
            if os.path.isdir(path_to_file):
                num_of_index_htmls += 1
                create_index_html(path_to_file, deep + 1)
        except OSError:
            print "WARNING: ACCESS DENIED! " + path_to_file
            num_of_index_htmls -= 1
            continue

        filelist.append( Data(filename, current_directory, deep) )

        # -v or --verbose should be changeable
        print filelist[-1] # BUG: ha a felhasználó / jelet ad meg a futtatáskor a mappára, akkor // lesz a kimeneten!

    # see __cmp__ function of Data class
    filelist.sort()

    # increase the processed_files counter by the number of the
    # files and directories in the current directory
    global processed_files
    processed_files += len(filelist)-1

    context = {
        'datas' : filelist,
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



def main():
    print "Static HTML file browser for Dropbox"

    parser = argparse.ArgumentParser()
    parser.add_argument("location",
                        help="relative or absolute path to your Public dropbox folder")
    # group is used for mutual exclusion of installing and cleaning up
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--install",
                        action="store_true",
                        help="prepares your Dropbox folder by copying icons to the specified directory.\
                              This directory can be set up in config.py configuration file")
    group.add_argument("-clean",
                        action="store_true",
                        help="cleans your Dropbox directory by deleting index.html files")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="verbose output STILL NOT IMPLEMENTED")
    args = parser.parse_args()

    if args.install:
        install(config.INSTALL_DIR)
    if args.clean:
        cleanup(config.INSTALL_DIR)
        exit(0)
    

    global PATH
    PATH = args.location
    create_index_html(PATH)
    print "Total processed files and directories: {n}".format(n=processed_files)
    print "Total index.html files generated: {n}".format(n=num_of_index_htmls)


#############################################################################

if __name__ == "__main__":
    main()
