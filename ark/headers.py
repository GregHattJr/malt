# --------------------------------------------------------------------------
# Handles header-parser callbacks.
# --------------------------------------------------------------------------


# Stores a list of registered parser callbacks.
_parsers = []


def register(callback):

    """ Decorator function for registering header-parser callbacks.

    A header-parser callback should accept a single string argument containing
    the raw content of a source file. It should return three values:

     i) A boolean indicating whether or not it has handled the file.
    ii) None, or, if handled, a string containing the file's text content.
    ii) None, or, if handled, a dictionary containing the file's metadata.

    """

    _parsers.append(callback)
    return callback


# Parses a source file's raw content and returns its text and metadata.
def parse(raw_text):
    for parser in _parsers:
        handled, text, meta = parser(raw_text)
        if handled:
            return text, normalize(meta)
    return raw_text, {}


# Returns a normalized metadata dictionary.
def normalize(meta):
    output = {}
    for key, value in meta.items():
        output[key.lower().replace(' ', '_').replace('-', '_')] = value
    return output
