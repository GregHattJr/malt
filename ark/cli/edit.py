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

  Ark will launch the editor specified by i) the $ARK_EDITOR environment
  variable, or ii) the $EDITOR environment variable. If neither variable
  exists it will attempt to use vim.

Arguments:
  <type>              Record type, e.g. 'posts'.
  <file...>           Record filename(s).

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    args = parser.get_args()
    if len(args) < 2:
        sys.exit("Error: the 'edit' command requires at least 2 arguments.")

    paths = [ark.site.src('[%s]' % args[0], path) for path in args[1:]]

    for path in paths:
        if not os.path.exists(path):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            template = "---\ntitle: Record Title\ndate: %s\n---\n\n\n"
            ark.utils.writefile(path, template % now)

    editor = os.getenv('ARK_EDITOR') or os.getenv('EDITOR') or 'vim'
    if not shutil.which(editor):
        sys.exit("Error: cannot locate the editor '%s'." % editor)

    paths.insert(0, editor)
    subprocess.call(paths)
