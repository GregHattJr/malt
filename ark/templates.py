# --------------------------------------------------------------------------
# This module handles template-engine callbacks.
# --------------------------------------------------------------------------

import sys

from . import site
from . import utils


# Stores registered template-engine callbacks indexed by file extension.
callbacks = {}


# Caches a list of the theme's template files.
cache = None


# Decorator function for registering template-engine callbacks. A template-
# engine callback should accept a page object and a template filename and
# return a string of html.
#
# Callbacks are registered per file extension, e.g.
#
#   @ark.templates.register('ibis')
#   def callback(page, filename):
#       ...
#       return html
#
def register(ext):

    def register_callback(callback):
        callbacks[ext] = callback
        return callback

    return register_callback


# Render the supplied page object into html.
def render(page):

    # Cache a list of the theme's template files for future calls.
    global cache
    if cache is None:
        cache = utils.files(site.theme('templates'))

    # Find the first template file matching the page's template list.
    for name in page['templates']:
        for finfo in cache:
            if name == finfo.base:
                if finfo.ext in callbacks:
                    return callbacks[finfo.ext](page, finfo.name)
                else:
                    sys.exit(
                        "Error: unrecognised template extension '.%s'." % finfo.ext
                    )

    # Missing template file. Print an error message and exit.
    sys.exit(
        "Error: missing template file.\n\n  Page: %s\n  Templates: %s" % (
            page['path'], ', '.join(page['templates'])
        )
    )
