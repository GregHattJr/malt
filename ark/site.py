# --------------------------------------------------------------------------
# Loads, processes, and stores the site's configuration data.
# --------------------------------------------------------------------------

import os
import time
import sys

from . import utils


# Stores the site's configuration data.
config = {}


# Initialize the site model.
def init():

    # Record the start time.
    config['_start_'] = time.time()

    # Initialize a count of the number of pages rendered.
    config['_rendered_'] = 0

    # Initialize a count of the number of pages written to disk.
    config['_written_'] = 0

    # Load the site's configuration file.
    load_site_config()


# Attempts to determine the path to the site's home directory. Returns an empty
# string if the directory cannot be located.
def find_home():
    path = os.getcwd()
    while os.path.isdir(path):
        if os.path.isfile(os.path.join(path, '.ark')):
            return os.path.abspath(path)
        path = os.path.join(path, '..')
    return ''


# Attempts to determine the path to the theme directory corresponding to
# the specified theme name. Exits with an error message on failure.
def find_theme(name):

    # A directory in the site's theme library?
    if os.path.isdir(lib(name)):
        return lib(name)

    # A directory in the global theme library?
    if os.getenv('ARK_THEMES'):
        if os.path.isdir(os.path.join(os.getenv('ARK_THEMES'), name)):
            return os.path.join(os.getenv('ARK_THEMES'), name)

    # A raw directory path?
    if os.path.isdir(name):
        return name

    # A bundled theme directory in the application folder?
    bundled = os.path.join(os.path.dirname(__file__), 'ini', 'lib', name)
    if os.path.isdir(bundled):
        return bundled

    sys.exit("Error: cannot locate the theme directory '%s'." % name)


# Provides access to the site's normalized record-type data. Returns the
# entire dictionary of type data if no key is specified.
def types(rectype, key=None):
    typesdict = config.setdefault('_types_', {})

    # Set default values for any missing type data.
    if not rectype in typesdict:
        typesdict[rectype] = {
            'name': rectype,
            'title': utils.titlecase(rectype),
            'slug': '' if rectype == 'pages' else utils.slugify(rectype),
            'tag_slug': 'tags',
            'indexed': False if rectype == 'pages' else True,
            'order_by': 'date',
            'reverse': True,
            'per_index': 10,
            'per_tag_index': 10,
            'homepage': False,
        }
        typesdict[rectype].update(config.get(rectype, {}))

    if key:
        return typesdict[rectype][key]
    else:
        return typesdict[rectype]


# Returns the path to the site's home directory or an empty string if the
# home directory cannot be located. Appends arguments.
def home(*append):
    path = config.get('_home_') or config.setdefault('_home_', find_home())
    return os.path.join(path, *append)


# Returns the path to the source directory. Appends arguments.
def src(*append):
    path = config.get('_src_') or config.setdefault('_src_', home('src'))
    return os.path.join(path, *append)


# Returns the path to the output directory. Appends arguments.
def out(*append):
    path = config.get('_out_') or config.setdefault('_out_', home('out'))
    return os.path.join(path, *append)


# Returns the path to the theme-library directory. Appends arguments.
def lib(*append):
    path = config.get('_lib_') or config.setdefault('_lib_', home('lib'))
    return os.path.join(path, *append)


# Returns the path to the extensions directory. Appends arguments.
def ext(*append):
    path = config.get('_ext_') or config.setdefault('_ext_', home('ext'))
    return os.path.join(path, *append)


# Returns the path to the includes directory. Appends arguments.
def inc(*append):
    path = config.get('_inc_') or config.setdefault('_inc_', home('inc'))
    return os.path.join(path, *append)


# Returns the path to the theme directory. Appends arguments.
def theme(*append):
    if '_themepath_' in config:
        return os.path.join(config['_themepath_'], *append)
    else:
        path = config.setdefault('_themepath_', find_theme(config['theme']))
        return os.path.join(path, *append)


# Returns the output slug list for the specified record type.
def slugs(rectype, *append):
    typeslug = types(rectype, 'slug')
    sluglist = [typeslug] if typeslug else []
    sluglist.extend(append)
    return sluglist


# Returns the URL corresponding to the specified slug list.
def url(slugs):
    return '@root/' + '/'.join(slugs) + '//'


# Returns the paged URL corresponding to the specified slug list.
def paged_url(slugs, page_number, total_pages):
    if page_number == 1:
        return url(slugs + ['index'])
    elif 2 <= page_number <= total_pages:
        return url(slugs + ['page-%s' % page_number])
    else:
        return ''


# Returns the URL of the index page of the specified record type.
def index_url(rectype):
    if types(rectype, 'indexed'):
        if types(rectype, 'homepage'):
            return url(['index'])
        else:
            return url(slugs(rectype, 'index'))
    else:
        return ''


# Returns the record type corresponding to a source file or directory path.
def type_from_src(srcpath):
    slugs = os.path.relpath(srcpath, src()).replace('\\', '/').split('/')
    return slugs[0].strip('[]')


# Returns the output slug list for the specified source directory.
def slugs_from_src(srcdir, *append):
    rectype = type_from_src(srcdir)
    dirnames = os.path.relpath(srcdir, src()).replace('\\', '/').split('/')
    sluglist = slugs(rectype)
    sluglist.extend(utils.slugify(dirname) for dirname in dirnames[1:])
    sluglist.extend(append)
    return sluglist


# Returns the application runtime in seconds.
def runtime():
    return time.time() - config['_start_']


# Increments the count of pages rendered by n and returns the new value.
def rendered(n=0):
    config['_rendered_'] += n
    return config['_rendered_']


# Increments the count of pages written by n and returns the new value.
def written(n=0):
    config['_written_'] += n
    return config['_written_']


# Loads and normalizes the site's configuration data.
def load_site_config():

    # Load the default site configuration file.
    path = os.path.join(os.path.dirname(__file__), 'config.py')
    with open(path, encoding='utf-8') as file:
        exec(file.read(), config)

    # Load the custom site configuration file.
    if home() and os.path.isfile(home('config.py')):
        with open(home('config.py'), encoding='utf-8') as file:
            exec(file.read(), config)

    # Delete the __builtins__ attribute as it pollutes variable dumps.
    del config['__builtins__']

    # If 'root' isn't an empty string, make sure it ends in a slash.
    if config['root'] and not config['root'].endswith('/'):
        config['root'] += '/'
