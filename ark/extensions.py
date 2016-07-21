# --------------------------------------------------------------------------
# Finds and loads extensions.
# --------------------------------------------------------------------------

import os
import sys
import importlib

from . import site
from . import cli


# Stores a dictionary of loaded extension modules.
_loaded = {}


# Load any Python modules found in the extensions directories.
def load():

    # List of directories to search for extensions.
    extdirs = []

    # Default extensions bundled with Ark.
    extdirs.append(os.path.join(os.path.dirname(__file__), 'ext'))

    # Global extensions directory/directories.
    if os.getenv('ARK_EXT') and not cli.parser['no-global-ext']:
        for path in os.getenv('ARK_EXT').split(os.pathsep):
            if os.path.isdir(path):
                extdirs.append(path)

    # Site extensions.
    if os.path.isdir(site.ext()) and not cli.parser['no-site-ext']:
        extdirs.append(site.ext())

    # Theme extensions.
    if os.path.isdir(site.theme('code')) and not cli.parser['no-theme-ext']:
        extdirs.append(site.theme('code'))

    # Load extensions. This gets a little messy because we're allowing for
    # 'dev-friendly' plugin loading. An item in an extension directory can
    # be a python module or package *or* a directory containing a module or
    # package along with its readme, license file, etc.
    for extdir in extdirs:
        for item in os.listdir(extdir):
            itembase = os.path.splitext(item)[0]
            itemslug = itembase.replace('-', '_')
            itempath = os.path.join(extdir, item)

            # Skip hidden/packaging files.
            if item[0] in '_.' or itembase == 'readme':
                continue

            # Is the item a directory?
            if os.path.isdir(itempath):

                # Does the item directory contain an extension package?
                if os.path.isdir(os.path.join(itempath, itemslug)):
                    _load(itempath, itemslug)

                # Does the item directory contain an extension module?
                elif os.path.isfile(os.path.join(itempath, itemslug + '.py')):
                    _load(itempath, itemslug)

                # The item directory itself must be the extension package.
                else:
                    _load(extdir, item)

            # The item is a file. Assume it's a Python module.
            else:
                _load(extdir, itembase)


# Load the named module from the specified directory.
def _load(directory, module):
    sys.path.insert(0, directory)
    _loaded[module] = importlib.import_module(module)
    sys.path.pop(0)


# Returns the dictionary of loaded extension modules.
def loaded():
    return _loaded
