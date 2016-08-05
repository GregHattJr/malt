# --------------------------------------------------------------------------
# This module loads and preprocesses source files.
# --------------------------------------------------------------------------

from . import renderers
from . import utils
from . import hooks


# Assemble a list of source files in the specified directory. A file is only
# included if a renderer has been registered for its extension.
def srcfiles(directory):
    files = utils.files(directory)
    extensions = renderers.extensions()
    return [finfo for finfo in files if finfo.ext in extensions]


# Load a source file. File metadata (e.g. yaml headers) can be extracted by
# preprocessor callbacks registered on the 'file_text' filter hook.
def load(filepath):
    with open(filepath, encoding='utf-8') as file:
        text, meta = file.read(), {}
    text = hooks.filter('file_text', text, meta)
    return text, normalize(meta)


# Normalize a metadata dictionary's keys.
def normalize(meta):
    output = {}
    for key, value in meta.items():
        output[key.lower().replace(' ', '_').replace('-', '_')] = value
    return output
