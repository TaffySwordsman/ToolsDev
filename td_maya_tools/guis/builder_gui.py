#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    asy160030
    bkp170130
    bmc180001

:synopsis:
    Contains the logic for the GUI used by stacker

:description:
    This module creates a GUI for the code in the stacker module and adds additional
    functionality. When the user presses the 'Make Stacks' button, the GUI will verify
    it has all the necessary information to create stacks, and will then create stacks by
    duplicating geometry from the three sectioned out groups (base, middle, top).
    A random object from the base selection will used to make the base, a random object
    from the middle selection to form the middle of the stack, and a random object from
    the top selection will be placed at the top.  The user will receive text feedback in
    the GUI based on the selections they set.

:applications:
    Maya

:see_also:
    stacker.py
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
