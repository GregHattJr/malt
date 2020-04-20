# --------------------------------------------------------------------------
# This extension adds support for dropcaps to record files.
# --------------------------------------------------------------------------

import malt
import re


# Regex for locating dropcaps.
regex = re.compile(r'\[(.)\]')


# Register our callback on the 'record_html' filter.
@malt.hooks.register('record_html')
def dropcaps(text, record):
    return regex.sub(r'<span class="dropcap">\1</span>', text)
