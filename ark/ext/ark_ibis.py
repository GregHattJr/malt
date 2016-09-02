# --------------------------------------------------------------------------
# This extension adds support for Ibis templates.
# --------------------------------------------------------------------------

import sys
from ark import hooks, templates, site

try:
    import ibis
except ImportError:
    ibis = None


# The ibis package is an optional dependency.
if ibis:

    # Initialize our Ibis template loader on the 'init' event hook.
    @hooks.register('init')
    def init():
        ibis.config.loader = ibis.loaders.FileLoader(site.theme('templates'))

    # Register our template engine callback for files with a .ibis extension.
    @templates.register('ibis')
    def callback(page, filename):
        try:
            template = ibis.config.loader(filename)
            return template.render(page)
        except ibis.errors.TemplateError as e:
            msg =  "-----------------------\n"
            msg += "  Ibis Template Error  \n"
            msg += "-----------------------\n\n"
            msg += "  Template: %s\n" % filename
            msg += "  Page:     %s\n\n" % page['path']
            msg += "  %s: %s" % (e.__class__.__name__, e)
            if e.__context__:
                msg += "\n\nThe following exception was reported:\n\n"
                msg += "%s: %s" % (
                    e.__context__.__class__.__name__, e.__context__
                )
            sys.exit(msg)
