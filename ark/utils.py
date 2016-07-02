# --------------------------------------------------------------------------
# Utility functions.
# --------------------------------------------------------------------------

import collections
import os
import unicodedata
import re
import shutil
import datetime


# Named tuples for file and directory information.
DirInfo = collections.namedtuple('DirInfo', 'path, name')
FileInfo = collections.namedtuple('FileInfo', 'path, name, base, ext')


# Returns a list of subdirectories of the specified directory.
def subdirs(directory):
    directories = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            directories.append(DirInfo(path, name))
    return directories


# Returns a list of files in the specified directory.
def files(directory):
    files = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            files.append(fileinfo(path))
    return files


# Returns a FileInfo instance for the specified filepath.
def fileinfo(path):
    name = os.path.basename(path)
    base, ext = os.path.splitext(name)
    return FileInfo(path, name, base, ext.strip('.'))


# Returns the creation time of the specified file. This function works on OSX,
# BSD, and Windows. On Linux it returns the time of the file's last metadata
# change.
def get_creation_time(path):
    stat = os.stat(path)
    if hasattr(stat, 'st_birthtime') and stat.st_birthtime:
        return datetime.datetime.fromtimestamp(stat.st_birthtime)
    else:
        return datetime.datetime.fromtimestamp(stat.st_ctime)


# Slug preparation function. Used to sanitize url components, etc.
def slugify(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = s.replace("'", '')
    s = re.sub(r'[^a-z0-9-]+', '-', s)
    s = re.sub(r'--+', '-', s)
    return s.strip('-')


# Returns a titlecased version of the supplied string.
def titlecase(s):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda m: m.group(0)[0].upper() + m.group(0)[1:],
        s
    )


# Copies the contents of 'srcdir' to 'dstdir'.
#
#   * Creates the destination directory if necessary.
#   * If skiptypes is true, will skip [type] directories.
#   * If noclobber is true, will avoid overwriting existing files.
#
def copydir(srcdir, dstdir, skiptypes=False, noclobber=False):

    if not os.path.exists(srcdir):
        return

    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    for name in os.listdir(srcdir):
        src = os.path.join(srcdir, name)
        dst = os.path.join(dstdir, name)

        if skiptypes and name.startswith('[') and name.endswith(']'):
            continue

        if name in ('__pycache__', '.DS_Store'):
            continue

        if os.path.isfile(src):
            copyfile(src, dst, noclobber)

        elif os.path.isdir(src):
            copydir(src, dst, skiptypes, noclobber)


# Copies the file 'src' as 'dst'.
#
# If 'noclobber' is true, this function will not overwrite an existing 'dst'.
#
# This function attempts to avoid unnecessarily overwriting existing files with
# identical copies. If 'dst' exists and has the same size and mtime as 'src',
# 'dst' will left in place. (The goal here is to avoid unnecessary SSD writes
# when running the 'build' command in a loop.)
def copyfile(src, dst, noclobber=False):
    if os.path.isfile(dst):
        if noclobber:
            return
        if os.path.getmtime(src) == os.path.getmtime(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                return

    shutil.copy2(src, dst)


# Clears the contents of a directory.
def cleardir(dirpath):
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


# Writes a string to a file. Creates parent directories if required.
def writefile(path, content):
    path = os.path.abspath(path)

    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


# Creates a redirect page at the specified filepath.
def make_redirect(filepath, url):
    html = """\
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="refresh" content="0; url=%s">
    </head>
    <body></body>
</html>
""" % url
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(html)
