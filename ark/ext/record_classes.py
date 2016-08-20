# --------------------------------------------------------------------------
# This extension adds support for user-defined record classes. Classes can
# be added as a comma-separated list via a 'classes' attribute.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark


# Register a callback on the 'page_classes' filter.
@ark.hooks.register('page_classes')
def add_classes(classes, page):
    if page['is_single'] and 'classes' in page['record']:
        if isinstance(page['record']['classes'], str):
            for userclass in page['record']['classes'].split(','):
                classes.append(userclass.strip())
    return classes
