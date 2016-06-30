# --------------------------------------------------------------------------
# Loads and processes files from the site's `inc` directory.
# --------------------------------------------------------------------------

import os

from . import loader
from . import renderers
from . import site


# Dictionary of rendered files indexed by file name.
_cache = None


# Returns a dictionary of rendered files from the `inc` directory.
def inc(key=None):

    # Lazy load the contents of the `inc` directory.
    global _cache
    if _cache is None:
        _cache = {}
        if os.path.isdir(site.inc()):
            for finfo in loader.srcfiles(site.inc()):
                text, _ = loader.load(finfo.path)
                key = finfo.base.lower().replace(' ', '_').replace('-', '_')
                _cache[key] = renderers.render(text, finfo.ext)

    # If a key has been specified, try to return the corresponding string.
    if key is not None:
        return _cache.get(key, None)

    # Otherwise, return the entire dictionary.
    return _cache
