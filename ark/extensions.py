# --------------------------------------------------------------------------
# Loads extension modules.
# --------------------------------------------------------------------------

import os
import sys
import importlib

from . import site
from . import cli


# Dictionary of loaded extension modules indexed by name.
loaded = {}


# Load the named module from the specified directory.
def load_module(directory, name):
    sys.path.insert(0, directory)
    loaded[name] = importlib.import_module(name)
    sys.path.pop(0)


# Load a directory of modules.
def load_directory(directory):
    for item in os.listdir(directory):
        if item.startswith('.'):
            continue
        itembase = os.path.splitext(item)[0]
        load_module(directory, itembase)


# Load Ark's default set of extensions.
def load_bundled():
    load_directory(os.path.join(os.path.dirname(__file__), 'ext'))


# Load extensions from the site directory.
def load_site():
    if os.path.isdir(site.ext()):
        load_directory(site.ext())


# Load installed extensions listed in the site's configuration file.
def load_installed():
    for name in site.config.get('extensions', []):
        loaded[name] = importlib.import_module(name)


# Load extensions bundled with the active theme.
def load_theme():
    if site.theme() and os.path.isdir(site.theme('code')):
        load_directory(site.theme('code'))


# Load bundled, installed, and site-directory extensions.
def load():
    load_bundled()
    load_installed()
    load_site()
