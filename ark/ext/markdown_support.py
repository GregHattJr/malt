# --------------------------------------------------------------------------
# This extension adds Markdown support to Ark.
#
# Files with a .md extension will be rendered as Markdown.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark
import markdown


# Check the config file for customized settings for the markdown renderer.
settings = ark.site.config.get('markdown', {})


# Initialize a markdown renderer.
mdrenderer = markdown.Markdown(**settings)


# Register a callback to render files with a .md extension.
@ark.renderers.register('md')
def render(text):
    return mdrenderer.reset().convert(text)
