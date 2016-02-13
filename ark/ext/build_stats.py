# --------------------------------------------------------------------------
# This extension prints a simple report at the end of each build.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark


# Register a callback on the 'exit' event hook.
@ark.hooks.register('exit')
def print_stats():

    # The site module maintains a count of the number of pages that have been
    # rendered into html and written to disk.
    rendered, written = ark.site.rendered(), ark.site.written()

    # We only want to print a report after a build run.
    if rendered == 0:
        return

    # The runtime() function gives the application's running time in seconds.
    time = ark.site.runtime()
    average = time / rendered

    # Print stats.
    print(
        "Rendered: %5d  |  Written: %5d  |  Time: %5.2f sec  |  Avg: %.4f sec/page" % (
            rendered, written, time, average
        )
    )
