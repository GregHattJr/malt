# --------------------------------------------------------------------------
# This extension adds support for source files in Markdown format. Files
# with a .md extension will be rendered as Markdown.
# --------------------------------------------------------------------------

import malt

try:
    import markdown
except ImportError:
    markdown = None


# The markdown package is an optional dependency.
if markdown:

    # Check the config file for custom settings for the markdown renderer.
    settings = malt.site.config.get('markdown', {})

    # Initialize a markdown renderer.
    renderer = markdown.Markdown(**settings)

    # Register a callback to render files with a .md extension.
    @malt.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)
