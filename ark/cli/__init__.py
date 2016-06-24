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
    cmd_build = parser.add_cmd("build", build.callback, build.helptext)
    cmd_build.add_flag("clear", "c")
    cmd_build.add_str_opt("out", None, "o")
    cmd_build.add_str_opt("src", None, "s")
    cmd_build.add_str_opt("lib", None, "l")
    cmd_build.add_str_opt("inc", None, "i")
    cmd_build.add_str_opt("ext", None, "e")
    cmd_build.add_str_opt("theme", None, "t")

    # Register the 'serve' command.
    cmd_serve = parser.add_cmd("serve", serve.callback, serve.helptext)
    cmd_serve.add_flag("no-browser")
    cmd_serve.add_str_opt("host", "localhost", "h")
    cmd_serve.add_int_opt("port", 8080, "p")

    # Register the 'init' command.
    cmd_init = parser.add_cmd("init", init.callback, init.helptext)
    cmd_init.add_flag("empty", "e")

    # Register the 'clear' command.
    parser.add_cmd("clear", clear.callback, clear.helptext)

    # Register the 'edit' command.
    parser.add_cmd("edit", edit.callback, edit.helptext)

    # Register the 'watch' command.
    parser.add_cmd("watch", watch.callback, watch.helptext)

    # Parse the application's command line arguments.
    parser.parse()
    if not parser.has_cmd():
      parser.help()
