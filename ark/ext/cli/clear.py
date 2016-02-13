# --------------------------------------------------------------------------
# Logic for the 'clear' command.
# --------------------------------------------------------------------------

import ark
import sys
import os


# Command help text.
helptext = """
Usage: %s clear [FLAGS]

  Clear the output directory.

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not os.path.exists(ark.site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    ark.utils.cleardir(ark.site.out())
