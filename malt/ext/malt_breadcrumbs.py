# --------------------------------------------------------------------------
# This extension assembles a 'breadcrumb trail' of links for each directory
# in a page's path.
# --------------------------------------------------------------------------

import malt
import os


# Register a callback on the 'init_record' hook to assemble a record's trail.
@malt.hooks.register('init_record')
def assemble_record_trail(record):
    typedata = malt.site.typedata(record['type'])
    record['crumbs'] = breadcrumb_trail(record['srcdir'], typedata)


# Register a callback on the 'render_page' hook to assemble a page's trail.
@malt.hooks.register('render_page')
def assemble_page_trail(page):
    if page['record']:
        page['crumbs'] = page['record']['crumbs']
    elif page['srcdir']:
        page['crumbs'] = breadcrumb_trail(page['srcdir'], page['type'])


# Assemble a breadcrumb trail for the specified source directory.
def breadcrumb_trail(srcdir, typedata):

    # We want to assemble separate trails of directory names and links.
    names, links = [], []

    # Begin with the root [type] directory.
    names.append(typedata['title'])
    if typedata['indexed']:
        url = malt.site.index_url(typedata['name'])
        link = '<a href="%s">%s</a>' % (url, typedata['title'])
        links.append(link)
    else:
        links.append(typedata['title'])

    # We need a list of directory names, excluding the root [type] directory.
    relpath = os.path.relpath(srcdir, malt.site.src())
    dirnames = relpath.replace('\\', '/').split('/')
    dirnames = dirnames[1:]

    # We need to maintain a list of corresponding directory slugs beginning
    # with the appropriate type slug.
    dirslugs = malt.site.slugs(typedata['name'])

    # Append to the trails for each directory in the list.
    for dirname in dirnames:
        names.append(dirname)
        dirslugs.append(malt.utils.slugify(dirname))
        url = malt.site.url(dirslugs + ['index'])
        link = '<a href="%s">%s</a>' % (url, dirname)
        links.append(link)

    return {'names': names, 'links': links}
