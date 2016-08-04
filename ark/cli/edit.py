# --------------------------------------------------------------------------
# Logic for the 'edit' command.
# --------------------------------------------------------------------------

import ark
import sys
import os
import datetime
import shutil
import subprocess


# Command help text.
helptext = """
Usage: %s edit [FLAGS] ARGUMENTS

  Edit a record file or files. This command will create new records if the
  named files do not exist.

  Ark will launch the editor specified by the $EDITOR environment variable
  if it exists, otherwise it will attempt to use vim.

Arguments:
  <file>...           Record filename(s).

Options:
  -t, --type <str>    Record type. Defaults to 'posts'.

Flags:
      --help          Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not parser.has_args():
        sys.exit("Error: missing argument.")

    root = '[%s]' % parser['type']
    paths = [ark.site.src(root, path) for path in parser.get_args()]

    for path in paths:
        if not os.path.exists(path):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            template = "---\ntitle: Record Title\ndate: %s\n---\n\n\n"
            ark.utils.writefile(path, template % now)

    editor = os.getenv('ARK_EDITOR') or os.getenv('EDITOR') or 'vim'
    if not shutil.which(editor):
        sys.exit("Error: cannot locate editor '%s'." % editor)

    paths.insert(0, editor)
    subprocess.call(paths)
