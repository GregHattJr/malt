# --------------------------------------------------------------------------
# Logic for the 'init' command.
# --------------------------------------------------------------------------

import os
import sys
import shutil

from .. import utils


# Command help text.
helptext = """
Usage: %s init [FLAGS] [ARGUMENTS]

  Initialize a new site directory. If a directory path is specified, that
  directory will be created and initialized. Otherwise, the current directory
  will be initialized. Existing files will not be overwritten.

Arguments:
  [directory]         Directory name. Defaults to the current directory.

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    arkdir = os.path.dirname(os.path.dirname(__file__))
    inidir = os.path.join(arkdir, 'ini')
    dstdir = parser.get_args()[0] if parser.has_args() else '.'
    os.makedirs(dstdir, exist_ok=True)
    os.chdir(dstdir)

    for name in ('ext', 'inc', 'lib', 'out', 'res', 'src'):
        os.makedirs(name, exist_ok=True)

    if not os.path.exists('ark.py'):
        shutil.copy2(os.path.join(inidir, 'ark.py'), 'ark.py')

    for name in ('ext', 'inc', 'src'):
        utils.copydir(os.path.join(inidir, name), name, noclobber=True)

    for dirinfo in utils.subdirs(os.path.join(inidir, 'lib')):
        if not dirinfo.name in ('debug'):
            theme = os.path.join('lib', dirinfo.name)
            utils.copydir(dirinfo.path, theme, noclobber=True)
