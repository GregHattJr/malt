# --------------------------------------------------------------------------
# Processes the application's command-line arguments.
# --------------------------------------------------------------------------

import os
import clio
import sys

from . import build
from . import init
from . import clear
from . import serve
from . import edit
from . import watch

from .. import meta


# We want the root ArgParser instance to be globally available.
parser = None


# Application help text.
helptext = """
Usage: %s [FLAGS] [COMMAND]

  Ark is a static website generator. It transforms a directory of text files
  into a self-contained website that can be viewed locally or served remotely.

Flags:
  --help              Print the application's help text and exit.
  --version           Print the application's version number and exit.

Commands:
  build               Build the site.
  clear               Clear the output directory.
  edit                Edit an existing record or create a new record file.
  init                Initialize a new site directory.
  serve               Run a web server on the site's output directory.
  watch               Monitor the site directory and rebuild on changes.

Command Help:
  help <command>      Print the specified command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Parse the application's command-line arguments.
def parse():
    global parser

    # Root parser.
    parser = clio.ArgParser(helptext, meta.__version__)
    parser.add_flag("no-global-ext")
    parser.add_flag("no-site-ext")

    # Register the 'build' command.
    cmd_build = parser.add_cmd("build", build.helptext, build.callback)
    cmd_build.add_flag("clear c")
    cmd_build.add_str("out o", None)
    cmd_build.add_str("src s", None)
    cmd_build.add_str("lib l", None)
    cmd_build.add_str("inc i", None)
    cmd_build.add_str("ext e", None)
    cmd_build.add_str("theme t", None)

    # Register the 'serve' command.
    cmd_serve = parser.add_cmd("serve", serve.helptext, serve.callback)
    cmd_serve.add_flag("no-browser")
    cmd_serve.add_str("host h", "localhost")
    cmd_serve.add_int("port p", 0)

    # Register the 'init' command.
    cmd_init = parser.add_cmd("init", init.helptext, init.callback)
    cmd_init.add_flag("empty e")

    # Register the 'clear' command.
    parser.add_cmd("clear", clear.helptext, clear.callback)

    # Register the 'edit' command.
    parser.add_cmd("edit", edit.helptext, edit.callback)

    # Register the 'watch' command.
    parser.add_cmd("watch", watch.helptext, watch.callback)

    # Parse the application's command line arguments.
    parser.parse()
