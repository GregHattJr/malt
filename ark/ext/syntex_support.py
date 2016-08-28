# --------------------------------------------------------------------------
# This extension adds support for source files in Syntex format. Files with
# a .stx extension will be rendered as Syntex.
# --------------------------------------------------------------------------

import ark
import syntex


# Register a callback to render files with a .stx extension.
@ark.renderers.register('stx')
def render(text):
    return syntex.render(text, pygmentize=True)
