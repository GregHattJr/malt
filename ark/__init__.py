# --------------------------------------------------------------------------
# Ark: a static website generator in Python.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import sys


# Ark requires at least Python 3.4.
if sys.version_info < (3, 4):
    sys.exit('Error: Ark requires Python >= 3.4.')


# Template for error messages informing the user of any missing libraries.
error = """Error: Ark requires the %s library. Try:

    $ pip install %s"""


# Check that all the application's dependencies are available.
try:
    import yaml
except ImportError:
    sys.exit(error % ('PyYaml', 'pyyaml'))


try:
    import markdown
except ImportError:
    sys.exit(error % ('Markdown', 'markdown'))


try:
    import syntex
except ImportError:
    sys.exit(error % ('Syntex', 'syntex'))


try:
    import ibis
except ImportError:
    sys.exit(error % ('Ibis', 'ibis'))


try:
    import pygments
except ImportError:
    sys.exit(error % ('Pygments', 'pygments'))


try:
    import clio
except ImportError:
    sys.exit(error % ('Clio', 'libclio'))


try:
    import shortcodes
except ImportError:
    sys.exit(error % ('Shortcodes', 'shortcodes'))


try:
    import jinja2
except ImportError:
    sys.exit(error % ('Jinja', 'jinja2'))


# We import the package's modules so users can access 'ark.foo' via a simple
# 'import ark' statement. Otherwise the user would have to import each module
# individually as 'import ark.foo'.
from . import build
from . import cli
from . import extensions
from . import hashes
from . import hooks
from . import includes
from . import loader
from . import meta
from . import pages
from . import records
from . import renderers
from . import site
from . import templates
from . import utils


# The main() function is the application's entry point. Calling main()
# initializes the site model, loads the site's plugins, and fires a series of
# event hooks. All of the application's functionality is handled by callbacks
# registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Process the application's command-line arguments.
    cli.parse()

    # Load plugins.
    extensions.load()

    # Fire the 'init' event. (Runs callbacks registered on the 'init' hook.)
    hooks.event('init')

    # Fire the 'main' event. (Runs callbacks registered on the 'main' hook.)
    hooks.event('main')

    # Fire the 'exit' event. (Runs callbacks registered on the 'exit' hook.)
    hooks.event('exit')
