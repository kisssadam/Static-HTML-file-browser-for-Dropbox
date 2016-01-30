import os
import config
from shutil import copytree, rmtree


def is_answer_yes(answer):
    """Returns True if answer is yes, False otherwise"""

    answer = answer.lower()
    return answer == 'yes' or answer == 'y'


def ask_yes_no_question(question):
    """Writes question to stdout and returns True or False depending on the answer"""

    result = "no"
    try:
        result = raw_input(question + " (yes/no) ")
    except (EOFError, KeyboardInterrupt):
        print   # prints a new line
        exit(1) # terminates the program
    return result


def is_config_already_set_up():
    """Checks if the user already set up config.py"""

    return is_answer_yes(ask_yes_no_question("Did you configured config.py?"))


def install(path_to_public_directory):
    """
    This function is called, when we run the program with '-i' or '--install'
    """

    destination = os.path.join(path_to_public_directory, "icons")

    # before the installation you have to set up your own config.py configuration
    if not is_config_already_set_up():
        print "Before running this program, you have to edit config.py with a text editor!"
        exit(0)

    # checking for resources to be installed
    # if icons are missing, we have nothing to install
    if not os.path.isdir("icons"):
        print "Cannot find local icons folder!"
        exit(1)

    # if destination directory exists, ask user what to do: overwrite or exit
    if os.path.isdir(destination):
        question = "Would you like to overwrite " + destination + " directory?"
        if is_answer_yes(ask_yes_no_question(question)):
            print "Removing " + destination
            rmtree(destination)
        else:
            print "No changes were made on the disk! Exiting..."
            return

    print "Copying resources to " + destination
    copytree("icons", destination)
    print "Installation successfully finished! Now check your " + destination + " folder!"


def mark_to_delete(path_to_starting_directory, file_to_remove):
    """
    Returns a list with path to every file_to_remove file starting from path_to_starting_directory.
    """

    files_to_remove = list()

    for dirpath, dirnames, filenames in os.walk(path_to_starting_directory):
        if "index.html" in filenames:
            files_to_remove.append(os.path.join(dirpath, file_to_remove))

    return files_to_remove

def cleanup(path_to_starting_directory):
    """
    This function removes the generated index.html files from path_to_starting_directory
    """

    print "Cleaning up index.html and icon files..."
    files_to_remove = mark_to_delete(path_to_starting_directory, "index.html")

    # get icons to delete
    if os.path.exists(config.DROPBOX_ICON_FOLDER):
        icons_to_delete = os.listdir(config.DROPBOX_ICON_FOLDER)
        icons_to_delete = [e for e in icons_to_delete if e != "index.html"]
        for e in icons_to_delete:
            files_to_remove.append(os.path.join(config.DROPBOX_ICON_FOLDER, e))

    number_of_files_to_remove = len(files_to_remove)
    if number_of_files_to_remove == 0:
        print path_to_starting_directory + " already cleaned up. There is nothing to remove."
        return

    print "The following files will be removed:"
    print "\n".join(files_to_remove)
    print "You are going to remove {count} files.".format(count = number_of_files_to_remove)

    # asking for user confirmation
    answer = ask_yes_no_question("Are you sure you want to continue? You cannot undo this operation!")
    if is_answer_yes(answer):
        for filename in files_to_remove:
            os.unlink(filename)

        # remove icon's folder
        if os.path.exists(config.DROPBOX_ICON_FOLDER):
            print "Removing " + config.DROPBOX_ICON_FOLDER
            os.rmdir(config.DROPBOX_ICON_FOLDER)
            print "Icon folder has been removed."

        # TODO: should look like this: number_of_removed_files / _number_of_files_to_remove
        print "You have removed {count} files.".format(count = number_of_files_to_remove)
    else:
        print "No files were removed!"
