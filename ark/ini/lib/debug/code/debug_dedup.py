# --------------------------------------------------------------------------
# This extension adds a dictionary deduplication filter to Ibis templates.
#
# The filter accepts an input dictionary and returns a copy with duplicate
# values marked as aliases.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ibis


@ibis.filters.register('dbdedup')
def dedup_dict(inputdict):
    outputdict = {}
    for k in sorted(inputdict):
        v = inputdict[k]
        if v is '' or v is None or isinstance(v, int) or isinstance(v, bool):
            outputdict[k] = v
            continue
        for outk, outv in outputdict.items():
            if v is outv:
                outputdict[k] = "<alias of [%s]>" % outk
                break
        if not k in outputdict:
            outputdict[k] = v
    return outputdict
