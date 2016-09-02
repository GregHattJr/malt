# --------------------------------------------------------------------------
# This extension adds support for shortcodes.
# --------------------------------------------------------------------------

import ark
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# The shortcodes package is an optional dependency.
if shortcodes:

    # Check the site's config file for customized settings for the shortcode
    # parser.
    settings = ark.site.config.get('shortcodes', {})

    # Initialize a single parser instance.
    parser = shortcodes.Parser(**settings)

    # Filter each node's content on the 'node_text' filter hook and render
    # any shortcodes contained in it.
    @ark.hooks.register('node_text')
    def render(text, node):
        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as e:
            msg =  "-------------------\n"
            msg += "  Shortcode Error  \n"
            msg += "-------------------\n\n"
            msg += "  Node: %s\n\n" % node.path()
            msg += "  %s: %s" % (e.__class__.__name__, e)
            if e.__context__:
                msg += "\n\nThe following exception was reported:\n\n"
                msg += "%s: %s" % (
                    e.__context__.__class__.__name__, e.__context__
                )
            sys.exit(msg)
