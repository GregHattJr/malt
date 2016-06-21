# --------------------------------------------------------------------------
# Logic for the 'build' command.
# --------------------------------------------------------------------------

import ark
import os
import sys


# Command help text.
helptext = """
Usage: %s build [FLAGS] [OPTIONS]

  Build the current site. This command can be run from the site directory or
  any of its subdirectories.

  The -t, --theme option can be used to override the theme specified in the
  site's configuration file. Its argument can be:

    1) A path to a theme directory.

    2) The name of a theme directory in the site's theme library or the
       global theme library specififed by the $ARK_THEMES environment
       variable.

    3) The name of a theme directory bundled with Ark itself, e.g. 'debug'.

Options:
  -e, --ext <path>      Override the default 'ext' directory.
  -i, --inc <path>      Override the default 'inc' directory.
  -l, --lib <path>      Override the default 'lib' directory.
  -o, --out <path>      Override the default 'out' directory.
  -s, --src <path>      Override the default 'src' directory.
  -t, --theme <name>    Override the theme specififed in the config file.

Flags:
  -c, --clear           Clear the output directory before building.
      --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if parser['out']: ark.site.config['_out_'] = parser['out']
    if parser['src']: ark.site.config['_src_'] = parser['src']
    if parser['lib']: ark.site.config['_lib_'] = parser['lib']
    if parser['inc']: ark.site.config['_inc_'] = parser['inc']
    if parser['ext']: ark.site.config['_ext_'] = parser['ext']

    if parser['theme']:
        ark.site.config['theme'] = parser['theme']

    if parser['clear']:
        ark.utils.cleardir(ark.site.out())

    @ark.hooks.register('main')
    def build_callback():
        if os.path.isdir(ark.site.src()):
            ark.build.build_site()
        else:
            sys.exit("Error: cannot locate the site's source directory.")
