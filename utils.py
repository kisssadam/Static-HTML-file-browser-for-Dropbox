import os
from shutil import copytree, rmtree


def sizeof_fmt(num):
    """
    Convert file size to human readable format.
    """
    if num == "-":
        return num

    num = float(num)
    for x in ['bytes','KB','MB','GB','TB',"PB","EX"]:
        if num < 1024.0 and x == 'bytes':
            return int(num)
        elif num < 1024.0:
            return "{0:.2f}&nbsp;{1}".format(num, x)
        num /= 1024.0


def fix_location(location):
    """
    Returns a location string that doesn't contains multiple
    "/" characters sequentially.
    """
    chars = list(location)
    fixed_chars = list()

    prev_char_is_slash = False
    for i in xrange(len(location)):
        if chars[i] == '/' and prev_char_is_slash:
            continue
        elif chars[i] == '/' and not prev_char_is_slash:
            fixed_chars.append(chars[i])
            prev_char_is_slash = True
        else:
            fixed_chars.append(chars[i])
            prev_char_is_slash = False

    return ''.join(fixed_chars)


def install(path):
    """
    This function is called, when we run the program with "-i" or "--install"
    """
    path += "/icons"
    print "Installing..."
    
    # before the installation everyone have to set up their own config.py
    try:
        answer = raw_input("Did you configured config.py? (yes/no) ")
    except (EOFError, KeyboardInterrupt):
            print   # prints a new line
            exit(1) # terminates the program

    if answer != "yes" and \
       answer != "y" and \
       answer !="z":
        print "Before running this program, you have to edit config.py with a text editor!"
        exit(0)

    # if the directory exists, then it will be deleted, and icons will be copied
    if os.path.isdir(path):
        try:
            answer = raw_input("Would you like to overwrite the entire " + path + " directory? (yes/no) ")
        except (EOFError, KeyboardInterrupt):
            print   # prints a new line
            exit(1) # terminates the program
        if answer == "yes" or \
           answer == "y" or \
           answer == "z":
            rmtree(path)
            copytree("icons", path)
            print "Installation successfully finished! Now check your " + path + " folder!"
        else:
            print "No changes were made on the disk! Exiting..."

    # if directory doesn't exists, then the program copies icons dir to Public folder
    elif os.path.isdir("icons"):
        copytree("icons", path)
        print "Installation successfully finished! Now check your " + path + " folder!"

    # can't find the icons folder in the same directory, where the program started
    else:
        sys.stderr.write("Cannot find local icons folder!\n")
        exit(1)


def mark_to_delete(current_directory):
    """
    Recursively creates a list with index.html files from the current_directory
    and returns the entire list. (These files can be deleted.)
    This function is used by the cleanup(starting_directory) function.
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


def cleanup(starting_directory):
    """
    This function is called when we run the program with "-del" parameter
    """

    print "Clearing up index.html files..."
    marked_to_delete = mark_to_delete(starting_directory)

    if len(marked_to_delete) == 0:
        print "There is nothing to remove. Exiting..."
        return

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
        return

