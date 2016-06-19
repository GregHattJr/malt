# --------------------------------------------------------------------------
# Logic for the 'init' command.
# --------------------------------------------------------------------------

import ark
import os
import sys
import shutil


# Command help text.
helptext = """
Usage: %s init [FLAGS] [ARGUMENTS]

  Initialize a new site directory. If a directory path is specified, that
  directory will be created and used. Otherwise, the current directory will be
  used. Existing files will not be overwritten.

Arguments:
  [directory]         Directory name. Defaults to the current directory.

Flags:
  -e, --empty         Do not create a skeleton site.
      --help          Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    arkdir = os.path.dirname(os.path.dirname(__file__))
    inidir = os.path.join(arkdir, 'ini')
    dstdir = parser.get_args()[0] if parser.has_args() else '.'
    os.makedirs(dstdir, exist_ok=True)
    os.chdir(dstdir)

    for name in ('ext', 'inc', 'lib', 'out', 'src'):
        os.makedirs(name, exist_ok=True)
    ark.utils.writefile('.ark', '')

    if parser['empty']:
        return

    if not os.path.exists('config.py'):
        shutil.copy2(os.path.join(inidir, 'config.py'), 'config.py')

    for name in ('ext', 'inc', 'src'):
        ark.utils.copydir(os.path.join(inidir, name), name, noclobber=True)

    for dirinfo in ark.utils.subdirs(os.path.join(inidir, 'lib')):
        if not dirinfo.name in ('debug'):
            theme = os.path.join('lib', dirinfo.name)
            ark.utils.copydir(dirinfo.path, theme, noclobber=True)
