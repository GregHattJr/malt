# --------------------------------------------------------------------------
# This extension adds support for YAML metadata headers in source files.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark
import re
import yaml


# Register our header-parser callback.
@ark.headers.register
def parse_yaml(raw_text):

    # Give the raw text a quick sniff before firing up the regex engine.
    if raw_text.startswith("---"):

        # A yaml header is identified by opening and closing `---` lines.
        match = re.match(r"^---\n(.*?\n)---\n+", raw_text, re.DOTALL)
        if match:
            text = raw_text[match.end(0):]
            meta = yaml.load(match.group(1))
            return True, text, meta if isinstance(meta, dict) else {}

    return False, None, None
