# --------------------------------------------------------------------------
# Loads, processes, and stores the site's configuration data.
# --------------------------------------------------------------------------

import os
import time
import sys

from . import utils


# Storage for the site's configuration data.
config = {}


# Storage for temporary data generated during the build process.
cache = {}


# Initialize the site model.
def init():

    # Record the start time.
    cache['start'] = time.time()

    # Initialize a count of the number of pages rendered.
    cache['rendered'] = 0

    # Initialize a count of the number of pages written to disk.
    cache['written'] = 0

    # Load the site's configuration file.
    load_site_config()


# Load and normalize the site's configuration data.
def load_site_config():

    # Default settings.
    config['root'] = ''
    config['theme'] = 'phoenix'
    config['extension'] = '.html'

    # Load the site configuration file.
    if home() and os.path.isfile(home('ark.py')):
        with open(home('ark.py'), encoding='utf-8') as file:
            exec(file.read(), config)

    # Delete the __builtins__ attribute as it pollutes variable dumps.
    if '__builtins__' in config:
        del config['__builtins__']

    # If 'root' isn't an empty string, make sure it ends in a slash.
    if config['root'] and not config['root'].endswith('/'):
        config['root'] += '/'


# Attempt to determine the path to the site's home directory. We check for
# the presence of either an 'ark.py' file or both 'src' and 'out' directories.
# We return an empty string if the home directory cannot be located.
def find_home():
    join, isdir, isfile = os.path.join, os.path.isdir, os.path.isfile
    path = os.getcwd()
    while isdir(path):
        if isfile(join(path, 'ark.py')):
            return os.path.abspath(path)
        elif isdir(join(path, 'src')) and isdir(join(path, 'out')):
            return os.path.abspath(path)
        path = join(path, '..')
    return ''


# Attempt to determine the path to the theme directory corresponding to
# the specified theme name. Exit with an error message on failure.
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

    sys.exit("Error: cannot locate theme directory '%s'." % name)


# Return the type-data dictionary for the specified record type. If a key is
# specified, the corresponding value is returned.
def typedata(rectype, key=None):
    types = cache.setdefault('types', {})

    # Set default values for any missing type data.
    if not rectype in types:
        types[rectype] = {
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
        types[rectype].update(config.get(rectype, {}))

    if key:
        return types[rectype][key]
    else:
        return types[rectype]


# Return a list of all record types in the site's source directory.
def typelist():
    types = []
    for _, name in utils.subdirs(src()):
        if name.startswith('['):
            types.append(name.strip('[]'))
    return types


# Return the path to the site's home directory or an empty string if the
# home directory cannot be located. Append arguments.
def home(*append):
    path = cache.get('home') or cache.setdefault('home', find_home())
    return os.path.join(path, *append)


# Return the path to the source directory. Append arguments.
def src(*append):
    path = cache.get('src') or cache.setdefault('src', home('src'))
    return os.path.join(path, *append)


# Return the path to the output directory. Append arguments.
def out(*append):
    path = cache.get('out') or cache.setdefault('out', home('out'))
    return os.path.join(path, *append)


# Return the path to the theme-library directory. Append arguments.
def lib(*append):
    path = cache.get('lib') or cache.setdefault('lib', home('lib'))
    return os.path.join(path, *append)


# Return the path to the extensions directory. Append arguments.
def ext(*append):
    path = cache.get('ext') or cache.setdefault('ext', home('ext'))
    return os.path.join(path, *append)


# Return the path to the includes directory. Append arguments.
def inc(*append):
    path = cache.get('inc') or cache.setdefault('inc', home('inc'))
    return os.path.join(path, *append)


# Return the path to the resources directory. Append arguments.
def res(*append):
    path = cache.get('res') or cache.setdefault('res', home('res'))
    return os.path.join(path, *append)


# Return the path to the theme directory. Append arguments.
def theme(*append):
    if 'themepath' in cache:
        return os.path.join(cache['themepath'], *append)
    else:
        path = cache.setdefault('themepath', find_theme(config['theme']))
        return os.path.join(path, *append)


# Return the output slug list for the specified record type. Append arguments.
def slugs(rectype, *append):
    typeslug = typedata(rectype, 'slug')
    sluglist = [typeslug] if typeslug else []
    sluglist.extend(append)
    return sluglist


# Return the URL corresponding to the specified slug list.
def url(slugs):
    return '@root/' + '/'.join(slugs) + '//'


# Return the paged URL corresponding to the specified slug list.
def paged_url(slugs, page_number, total_pages):
    if page_number == 1:
        return url(slugs + ['index'])
    elif 2 <= page_number <= total_pages:
        return url(slugs + ['page-%s' % page_number])
    else:
        return ''


# Return the URL of the index page of the specified record type.
def index_url(rectype):
    if typedata(rectype, 'indexed'):
        if typedata(rectype, 'homepage'):
            return url(['index'])
        else:
            return url(slugs(rectype, 'index'))
    else:
        return ''


# Return the record type corresponding to a source file or directory path.
def type_from_src(srcpath):
    slugs = os.path.relpath(srcpath, src()).replace('\\', '/').split('/')
    return slugs[0].strip('[]')


# Return the output slug list for the specified source directory.
def slugs_from_src(srcdir, *append):
    rectype = type_from_src(srcdir)
    dirnames = os.path.relpath(srcdir, src()).replace('\\', '/').split('/')
    sluglist = slugs(rectype)
    sluglist.extend(utils.slugify(dirname) for dirname in dirnames[1:])
    sluglist.extend(append)
    return sluglist


# Return the application runtime in seconds.
def runtime():
    return time.time() - cache['start']


# Increment the count of pages rendered by n and return the new value.
def rendered(n=0):
    cache['rendered'] += n
    return cache['rendered']


# Increment the count of pages written by n and return the new value.
def written(n=0):
    cache['written'] += n
    return cache['written']
