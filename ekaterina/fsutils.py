import os

def isdirectory(path):
    return os.path.isdir(path)

def isfile(path):
    return os.path.isfile(path)

def standardize_path(path):
    """Return shell-expanded version of the given path"""
    return os.path.abspath(os.path.expanduser(path))

def get_file_name(path, with_extension=False):
    """Given a path, return the filename"""
    if with_extension:
        return os.path.basename(path)
    else:
        return os.path.splitext(os.path.basename(path))[0]

def destination_path(dest, file_path, new_extension=None):
    """Given a file_path, return it's absolute path inside destination dest"""
    if not new_extension:
        return os.path.join(dest, get_file_name(file_path, with_extension=True))
    else:
        return os.path.join(dest,
                            "{}.{}".format(get_file_name(file_path),
                                           new_extension.lstrip(".")))
