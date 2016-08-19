# --------------------------------------------------------------------------
# This module makes the `ark` package directly executable.
#
# To run an `ark` package located on Python's import search path:
#
#   $ python -m ark
#
# To run an arbitrary `ark` package:
#
#   $ python /path/to/ark/package
#
# This latter form can be used for running development versions of Ark.
# --------------------------------------------------------------------------

import os
import sys


# Python doesn't automatically add the package's parent directory to the
# module search path so we need to do so manually before we can import `ark`.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


import ark
ark.main()
