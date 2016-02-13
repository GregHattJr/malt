# --------------------------------------------------------------------------
# Logic for the 'watch' command.
# --------------------------------------------------------------------------

import ark
import sys
import os
import hashlib
import time
import subprocess
import hashlib


# Command help text.
helptext = """
Usage: %s watch [FLAGS] [ARGUMENTS]

  Monitor the site directory and automatically rebuild the site when any file
  changes are detected.

  Arguments passed to this command will be passed along to the 'build'
  command. You can pass options or flags to the 'build' command by preceding
  them with '--'.

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Callback for the watch command. Python doesn't have a builtin file system
# watcher so we hack together one of our own.
def callback(parser):
    home = ark.site.home()
    args = [sys.argv[0], 'build', 'watching'] + parser.get_args()

    print("-" * 80)
    print("Site: %s" % home)
    print("Stop: Ctrl-C")
    print("-" * 80)

    # Build the site at least once with the 'watching' flag.
    subprocess.call(args + ['firstwatch'])
    print("-" * 80)

    # Create a hash digest of the site directory.
    oldhash = hashsite(home)

    # Loop until the user hits Ctrl-C.
    try:
        while True:
            newhash = hashsite(home)
            if newhash != oldhash:
                subprocess.call(args)
                newhash = hashsite(home)
            oldhash = newhash
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    # Build the site one last time without the 'watching' flag.
    print("\n" + "-" * 80)
    args.remove('watching')
    subprocess.call(args + ['lastwatch'])
    print("-" * 80)


# Returns a hash digest of the site directory.
def hashsite(sitedirpath):
    hash = hashlib.sha256()

    def hashdir(dirpath, is_home):
        for finfo in ark.utils.files(dirpath):
            mtime = os.path.getmtime(finfo.path)
            hash.update(str(mtime).encode())
            hash.update(finfo.name.encode())

        for dinfo in ark.utils.subdirs(dirpath):
            if is_home and dinfo.name in ('out'):
                continue
            hashdir(dinfo.path, False)

    hashdir(sitedirpath, True)
    return hash.digest()
