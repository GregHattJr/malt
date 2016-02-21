# --------------------------------------------------------------------------
# Loads and preprocesses source files.
# --------------------------------------------------------------------------

from . import renderers
from . import utils


# Stores a list of registered preprocessor callbacks.
_preprocessors = []


def register(callback):

    """ Decorator function for registering preprocessor callbacks.

    A preprocessor callback should accept two arguments: a string containing
    a source file's content and a dictionary containing metadata for that
    source file. It should return the processed string and updated dictionary.

    """

    _preprocessors.append(callback)
    return callback


# Returns a list of source files in the specified directory. A file is only
# included if a renderer has been registered for its extension.
def srcfiles(directory):
    files = utils.files(directory)
    registered = renderers.extensions()
    return [finfo for finfo in files if finfo.ext in registered]


# Loads and preprocesses a source file.
def load(filepath):
    with open(filepath, encoding='utf-8') as file:
        text, meta = file.read(), {}

    for callback in _preprocessors:
        text, meta = callback(text, meta)

    return text, normalize(meta)


# Normalizes a metadata dictionary's keys.
def normalize(meta):
    output = {}
    for key, value in meta.items():
        output[key.lower().replace(' ', '_').replace('-', '_')] = value
    return output
