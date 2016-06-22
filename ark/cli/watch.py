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

  Monitor the site directory and automatically rebuild when file changes are
  detected.

  Arguments passed to this command will be passed on to the 'build' command.
  Options intended for the 'build' command should be preceded by '--', e.g.

    ark watch -- --theme debug

  This prevents the options being parsed as options for the 'watch' command.

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
def hashsite(sitepath):
    hash = hashlib.sha256()

    def hashdir(dirpath, is_home):
        for fileinfo in ark.utils.files(dirpath):
            if fileinfo.name.endswith('~'):
                continue
            mtime = os.path.getmtime(fileinfo.path)
            hash.update(str(mtime).encode())
            hash.update(fileinfo.name.encode())

        for dirinfo in ark.utils.subdirs(dirpath):
            if is_home and dirinfo.name == 'out':
                continue
            hashdir(dirinfo.path, False)

    hashdir(sitepath, True)
    return hash.digest()
