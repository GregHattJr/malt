# --------------------------------------------------------------------------
# Application entry point.
# --------------------------------------------------------------------------

from . import site
from . import hooks
from . import extensions
from . import cli


# Calling main() initializes the site model, loads the site's plugins, and
# fires a series of event hooks. All of the application's functionality is
# handled by callbacks registered on these hooks.
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
