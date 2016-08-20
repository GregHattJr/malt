# --------------------------------------------------------------------------
# This extension adds support for user-defined record tags. Tags can be
# added as a comma-separated list via a 'tags' attribute.
# 
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark


# This dictionary maps tag-slugs to lists of record filepaths indexed by type.
tags = {}


# This dictionary maps tag-slugs to tag-names indexed by type.
names = {}


# A Tag instance pairs a tag-name with its corresponding tag-index url.
class Tag:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return 'Tag(name=%s, url=%s)' % (repr(self.name), repr(self.url))

    def __str__(self):
        return '<a href="%s">%s</a>' % (self.url, self.name)


# Register a callback on the 'init_record' event hook to process and register
# the record's tags.
@ark.hooks.register('init_record')
def register_tags(record):
    tagstr, record['tags'] = record.get('tags', ''), []
    for tag in (t.strip() for t in tagstr.split(',')):
        if tag:
            register_tag(record['type'], tag, record['src'])
            record['tags'].append(Tag(tag, url(record['type'], tag)))


# Register a callback on the 'exit_build' event hook to build the tag index
# pages.
@ark.hooks.register('exit_build')
def build_tag_indexes():

    # Iterate over the site's record types.
    for rectype, recmap in tags.items():

        # Fetch the type's configuration data.
        typedata = ark.site.typedata(rectype)

        # Iterate over the registered tags for the type.
        for slug, filelist in recmap.items():

            reclist = []
            for filepath in filelist:
                record = ark.records.record(filepath)
                if typedata['order_by'] in record:
                    reclist.append(record)

            index = ark.pages.Index(
                rectype,
                slugs(rectype, slug),
                reclist,
                typedata['per_tag_index']
            )

            index['tag'] = names[rectype][slug]
            index['is_tag_index'] = True

            index.render()


# Register a callback on the 'page_classes' filter to add tag classes.
@ark.hooks.register('page_classes')
def add_tag_classes(classes, page):
    if page.get('is_tag_index'):
        classes.append('tag-index')
        classes.append('tag-index-%s' % ark.utils.slugify(page['tag']))
    return classes


# Register a callback on the 'page_templates' filter to add tag templates.
@ark.hooks.register('page_templates')
def add_tag_templates(templates, page):
    if page.get('is_tag_index'):
        templates = [
            '%s-tag-index' % page['type']['name'],
            'tag-index',
            'index'
        ]
    return templates


# Register a new tag mapping.
def register_tag(rectype, tag, filepath):
    slug = ark.utils.slugify(tag)
    tags.setdefault(rectype, {}).setdefault(slug, []).append(filepath)
    names.setdefault(rectype, {}).setdefault(slug, tag)


# Returns the tag-index url for the specified tag.
def url(rectype, tag):
    return ark.site.url(slugs(rectype, tag, 'index'))


# Returns the output-slug list for the specified tag. Appends arguments.
def slugs(rectype, tag, *append):
    slugs = ark.site.slugs(rectype)
    slugs.append(ark.site.typedata(rectype, 'tag_slug'))
    slugs.append(ark.utils.slugify(tag))
    slugs.extend(append)
    return slugs
