# --------------------------------------------------------------------------
# This extension adds support for YAML metadata headers in source files.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark
import re
import yaml


# Register our preprocessor callback.
@ark.loader.register
def parse_yaml(text, meta):

    # Give the text a quick sniff before firing up the regex engine.
    if text.startswith("---\n"):

        # A yaml header is identified by opening and closing `---` lines.
        match = re.match(r"^---\n(.*?\n)---\n+", text, re.DOTALL)
        if match:
            text = text[match.end(0):]
            data = yaml.load(match.group(1))
            if isinstance(data, dict):
                meta.update(data)

    return text, meta
