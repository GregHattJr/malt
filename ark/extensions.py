# --------------------------------------------------------------------------
# Finds and loads extensions.
# --------------------------------------------------------------------------

import os
import sys
import importlib

from . import site
from . import cli


# Dictionary of loaded extension modules indexed by name.
loaded = {}


# Load Python modules and packages from the extensions directories.
def load():

    # List of directories to search for extensions.
    extdirs = []

    # 1. Default extensions bundled with Ark.
    extdirs.append(os.path.join(os.path.dirname(__file__), 'ext'))

    # 2. Global extensions directory (or directories).
    if os.getenv('ARK_EXT') and not cli.parser['no-global-ext']:
        for path in os.getenv('ARK_EXT').split(os.pathsep):
            if os.path.isdir(path):
                extdirs.append(path)

    # 3. Theme extensions directory.
    if os.path.isdir(site.theme('code')) and not cli.parser['no-theme-ext']:
        extdirs.append(site.theme('code'))

    # 4. Site extensions directory.
    if os.path.isdir(site.ext()) and not cli.parser['no-site-ext']:
        extdirs.append(site.ext())

    # Load extensions.
    for extdir in extdirs:
        for item in os.listdir(extdir):
            if item.startswith('.'):
                continue
            itembase = os.path.splitext(item)[0]
            load_module(extdir, itembase)


# Load the named module from the specified directory.
def load_module(directory, name):
    sys.path.insert(0, directory)
    loaded[name] = importlib.import_module(name)
    sys.path.pop(0)
