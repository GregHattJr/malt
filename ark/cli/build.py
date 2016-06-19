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

  The --theme option can be used to override the theme specified in the site's
  config file. Its argument can be either i) a path to a theme directory or
  ii) the name of a theme directory in the site's theme library or the global
  theme library specififed by the $ARK_THEMES environment variable.

  Arguments passed to this command are available as build flags to themes and
  plugins.

Options:
  -i, --inc <path>    Override the default 'inc' directory.
  -l, --lib <path>    Override the default 'lib' directory.
  -o, --out <path>    Override the default 'out' directory.
  -s, --src <path>    Override the default 'src' directory.
  -t, --theme <name>  Override the theme specififed in the config file.

Flags:
  -c, --clear         Clear the output directory before building.
      --help          Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if parser['out']: ark.site.setconfig('[out]', parser['out'])
    if parser['src']: ark.site.setconfig('[src]', parser['src'])
    if parser['lib']: ark.site.setconfig('[lib]', parser['lib'])
    if parser['inc']: ark.site.setconfig('[inc]', parser['inc'])

    if parser['theme']:
        ark.site.setconfig('[theme]', ark.site.find_theme(parser['theme']))

    if parser['clear']:
        ark.utils.cleardir(ark.site.out())

    ark.site.setconfig('[flags]', parser.get_args())

    @ark.hooks.register('main')
    def build_callback():
        if os.path.isdir(ark.site.src()):
            ark.build.build_site()
        else:
            sys.exit("Error: cannot locate the site's source directory.")
