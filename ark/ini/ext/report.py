# --------------------------------------------------------------------------
# This extension prints a simple status report at the end of each build.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

from ark import hooks, site


# Plugin version number.
__version__ = "1.0.0"


# Register a callback on the 'exit' event hook.
@hooks.register('exit')
def print_status_report():
    num_rendered, num_written = site.rendered(), site.written()

    # We only want to print a report after a build run.
    if num_rendered == 0:
        return

    # Singluar or plural?
    txt_rendered = "1 page" if num_rendered == 1 else "%s pages" % num_rendered
    txt_written = "1 page" if num_written == 1 else "%s pages" % num_written

    # The runtime() function gives the application's runtime in seconds.
    time = site.runtime()
    average = time / num_rendered

    # Default status report.
    f = "%s rendered, %s written in %.2f seconds. %.4f seconds per page."
    default = f % (txt_rendered, txt_written, time, average)

    # Compact report.
    f = "Rendered: %5d  |  Written: %5d  |  Time: %5.2f sec  |  Avg: %.4f sec/pg"
    compact = f % (num_rendered, num_written, time, average)

    # Print the compact version if the default is too long or if the 'watch'
    # command is running.
    if len(default) > 80:
        print(compact)
    elif 'watching' in site.flags() and not 'firstwatch' in site.flags():
        print(compact)
    else:
        print(default)
