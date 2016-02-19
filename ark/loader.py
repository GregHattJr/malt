# --------------------------------------------------------------------------
# Handles loading source files and parsing their metadata headers.
# --------------------------------------------------------------------------

from . import renderers
from . import headers
from . import utils


# Returns a list of source files in the specified directory. A file is only
# included if a renderer has been registered for its extension.
def srcfiles(directory):
    files = utils.files(directory)
    extensions = renderers.extensions()
    return [finfo for finfo in files if finfo.ext in extensions]


# Loads a source file and parses its metadata header.
def load(filepath):
    with open(filepath, encoding='utf-8') as file:
        return headers.parse(file.read())
