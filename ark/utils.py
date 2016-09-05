# --------------------------------------------------------------------------
# Utility functions.
# --------------------------------------------------------------------------

import collections
import os
import unicodedata
import re
import shutil
import datetime

from . import hooks


# Named tuples for file and directory information.
DirInfo = collections.namedtuple('DirInfo', 'path, name')
FileInfo = collections.namedtuple('FileInfo', 'path, name, base, ext')


# Return a list of subdirectories of the specified directory.
def subdirs(directory):
    directories = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            directories.append(DirInfo(entry.path, entry.name))
    return directories


# Return a list of files in the specified directory.
def files(directory):
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            files.append(fileinfo(entry.path))
    return files


# Return a FileInfo instance for the specified filepath.
def fileinfo(path):
    name = os.path.basename(path)
    base, ext = os.path.splitext(name)
    return FileInfo(path, name, base, ext.strip('.'))


# Return the creation time of the specified file. This function works on
# OSX, BSD, and Windows. On Linux it returns the time of the file's last
# metadata change.
def get_creation_time(path):
    stat = os.stat(path)
    if hasattr(stat, 'st_birthtime') and stat.st_birthtime:
        return datetime.datetime.fromtimestamp(stat.st_birthtime)
    else:
        return datetime.datetime.fromtimestamp(stat.st_ctime)


# Default slug-preparation function; returns a slugified version of the
# supplied string. This function is used to sanitize url components, etc.
def slugify(arg):
    out = unicodedata.normalize('NFKD', arg)
    out = out.encode('ascii', 'ignore').decode('ascii')
    out = out.lower()
    out = out.replace("'", '')
    out = re.sub(r'[^a-z0-9-]+', '-', out)
    out = re.sub(r'--+', '-', out)
    out = out.strip('-')
    return hooks.filter('slugify', out, arg)


# Return a titlecased version of the supplied string.
def titlecase(arg):
    out = re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda m: m.group(0)[0].upper() + m.group(0)[1:],
        arg
    )
    return hooks.filter('titlecase', out, arg)


# Copy the contents of 'srcdir' to 'dstdir'. The destination directory will
# be created if it does not already exist. If 'noclobber' is true, existing
# files will not be overwritten.
def copydir(srcdir, dstdir, noclobber=False):

    if not os.path.exists(srcdir):
        return

    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    for name in os.listdir(srcdir):
        src = os.path.join(srcdir, name)
        dst = os.path.join(dstdir, name)

        if name in ('__pycache__', '.DS_Store'):
            continue

        if os.path.isfile(src):
            copyfile(src, dst, noclobber)
        elif os.path.isdir(src):
            copydir(src, dst, noclobber)


# Copy the file 'src' as 'dst'. If 'noclobber' is true, an existing 'dst'
# file will not be overwritten. This function attempts to avoid
# unnecessarily overwriting existing files with identical copies. If 'dst'
# exists and has the same size and mtime as 'src', the copy will be aborted.
def copyfile(src, dst, noclobber=False):
    if os.path.isfile(dst):
        if noclobber:
            return
        if os.path.getmtime(src) == os.path.getmtime(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                return

    shutil.copy2(src, dst)


# Clear the contents of a directory.
def cleardir(dirpath):
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


# Write a string to a file. Creates parent directories if required.
def writefile(path, content):
    path = os.path.abspath(path)

    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
