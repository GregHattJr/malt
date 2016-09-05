# --------------------------------------------------------------------------
# Ark: a static website generator.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import sys


# Minimum Python version.
if sys.version_info < (3, 5):
    sys.exit('Error: Ark requires Python >= 3.5.')


# Template for error messages informing the user of any missing libraries.
error = """Error: Ark requires the %s library. Try:

    $ pip install %s"""


# Check that all the application's dependencies are available.
try:
    import clio
except ImportError:
    sys.exit(error % ('Clio', 'libclio'))


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
from . import theme
from . import utils


# The main() function is the application's entry point. Calling main()
# initializes the site model, loads the site's plugins, and fires a series of
# event hooks. All of the application's functionality is handled by callbacks
# registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Load bundled, installed, and site-directory plugins.
    extensions.load()

    # Process the application's command-line arguments.
    cli.parse()

    # Load theme plugins.
    theme.load()

    # Fire the 'init' event. (Runs callbacks registered on the 'init' hook.)
    hooks.event('init')

    # Fire the 'main' event. (Runs callbacks registered on the 'main' hook.)
    hooks.event('main')

    # Fire the 'exit' event. (Runs callbacks registered on the 'exit' hook.)
    hooks.event('exit')
