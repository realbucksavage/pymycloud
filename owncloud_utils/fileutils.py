import errno
import os


def create_file_if_needed(file_name):
    """
    Create a specified file if it doesn't exist
    :param file_name: The file to check and create
    """
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise
