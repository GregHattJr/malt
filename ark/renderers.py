# --------------------------------------------------------------------------
# This module handles text-to-html rendering-engine callbacks.
# --------------------------------------------------------------------------

import sys


# This dictionary maps file extensions to registered rendering engine
# callbacks. We include a default set of null renderers for various common
# file extensions. These can be overridden by plugins if desired.
_renderers = {
    'css': lambda s: s,
    'html': lambda s: s,
    'js': lambda s: s,
    'txt': lambda s: s,
}


def register(ext):

    """ Decorator function for registering rendering-engine callbacks.

    A rendering-engine callback should accept an input string and return
    a string containing the rendered html.

    Callbacks are registered per file extension, e.g.

        @ark.renderers.register('md')
        def callback(text):
            ...
            return rendered

    """

    def register_callback(callback):
        _renderers[ext] = callback
        return callback

    return register_callback


# Return a list of file extensions with registered renderers.
def extensions():
    return list(_renderers.keys())


# Render a string and return the result.
def render(text, ext):
    if ext in _renderers:
        return _renderers[ext](text)
    else:
        sys.exit("Error: no registered renderer for the '.%s' extension." % ext)
