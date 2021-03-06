# --------------------------------------------------------------------------
# Loads and processes files from the site's 'includes' directory.
# --------------------------------------------------------------------------

import os

from . import loader
from . import renderers
from . import site


# Dictionary of rendered files indexed by (normalized) filename.
cache = None


# Return a dictionary of rendered files from the 'includes' directory.
def load():

    # Load and cache the directory's contents.
    global cache
    if cache is None:
        cache = {}
        if os.path.isdir(site.inc()):
            for finfo in loader.srcfiles(site.inc()):
                text, _ = loader.load(finfo.path)
                key = finfo.base.lower().replace(' ', '_').replace('-', '_')
                cache[key] = renderers.render(text, finfo.ext)

    return cache
