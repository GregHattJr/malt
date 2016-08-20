# --------------------------------------------------------------------------
# This extension adds Markdown support to Ark. Files with a .md extension
# will be rendered as Markdown.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark
import markdown


# Check the config file for custom settings for the markdown renderer.
settings = ark.site.config.get('markdown', {})


# Initialize a markdown renderer.
renderer = markdown.Markdown(**settings)


# Register a callback to render files with a .md extension.
@ark.renderers.register('md')
def render(text):
    return renderer.reset().convert(text)
