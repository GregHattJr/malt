# --------------------------------------------------------------------------
# Loads source files and parses their front matter.
# --------------------------------------------------------------------------

import re
import yaml

from . import renderers
from . import utils


# Returns a list of source files in the specified directory. A file is only
# included if a renderer has been registered for its extension.
def srcfiles(directory):
    files = utils.files(directory)
    extensions = renderers.extensions()
    return [finfo for finfo in files if finfo.ext in extensions]


# Loads a source file and parses its header.
def load(filepath):
    with open(filepath, encoding='utf-8') as file:
        text, meta = file.read(), {}

    match = re.match(r"^---\n(.*?\n)[-.]{3}\n+", text, re.DOTALL)
    if match:
        text = text[match.end(0):]
        data = yaml.load(match.group(1))
        if isinstance(data, dict):
            for key, value in data.items():
                meta[key.lower().replace(' ', '_').replace('-', '_')] = value

    return text, meta
