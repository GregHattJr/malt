#!/usr/bin/env python3
# --------------------------------------------------------------------------
# Ark: a static website generator in Python.
#
# This script acts as the entry point for the development version of Ark; in
# general use, installing via pip will generate a custom entry point named
# 'ark' on the user's PATH.
#
# This script is named 'dark.py' partly because it runs the [d]evelopment
# version of Ark, but mostly because calling it 'ark.py' can lead to the
# application mistaking it for a site configuration file and entering an
# infinite self-importing spiral of death...
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import ark

# The main module contains the application's entry point.
ark.main.main()
