# --------------------------------------------------------------------------
# This module makes the `ark` package directly executable.
#
# If Ark has been installed using pip (i.e. if an `ark` package can be found
# in one of the standard import locations), then the following command will
# run this script in the installed `ark` package:
#
#   $ python -m ark
#
# Alternatively, an arbitrary, non-installed `ark` package can be run by
# omitting the -m flag and specifying the full path to the package
# directory:
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
