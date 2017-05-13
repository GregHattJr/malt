# --------------------------------------------------------------------------
# This module makes the `malt` package directly executable.
#
# To run an `malt` package located on Python's import search path:
#
#   $ python -m malt
#
# To run an arbitrary `malt` package:
#
#   $ python /path/to/malt/package
#
# This latter form can be used for running development versions of Malt.
# --------------------------------------------------------------------------

import os
import sys


# Python doesn't automatically add the package's parent directory to the
# module search path so we need to do so manually before we can import `malt`.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


import malt
malt.main()
