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
    functionality.
    When the user presses the 'Make Stacks' button, the GUI will verify it has all the
    necessary information to create stacks, and will then create stacks by duplicating
    geometry from the three sectioned out groups (base, middle, top).
    A random object from the base selection will used to make the base, a random object
    from the middle selection to form the middle of the stack, and a random object from
    the top selection will be placed at the top.
    The user will receive text feedback in the GUI based on the selections they set.

:applications:
    Maya

:see_also:
    stacker.py
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
from PySide2 import QtGui, QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# Imports That You Wrote
# N/A

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


def get_maya_window():
    """
    :return: A pointer to the Maya window
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#


class BuilderGUI:
    def __init__(self):
        """
        Accepts no arguments
        Declares all the variables that will be necessary for the GUI to function
        """
    def init_gui(self):
        """
        Accepts no arguments
        Adds three rows of buttons and line edits which will eventually display group info
            These buttons all connect to 'set_selection'
        A label and a line edit that allows the user to specify how many stacks to make
        A 'Make Stacks' button to make each stack by calling 'make_stacks'
        A 'Cancel' button, which calls 'self.close' to close the GUI
            (you don't need to write 'self.close', every GUI has it)
        """
    def set_selection(self):
        """
        Accepts no arguments
        Uses the sender to determine which button called it
        Updates the appropriate line edit with the transform of the selection that was set
        """
    def make_stacks(self):
        """
        Accepts no arguments
        Calls 'verify_args' to make sure the user has entered all necessary information
            If a None value is returned from 'verify_args', return None
        Uses a for loop to create the stacks
            Uses the 'random' Python library to pick a base, middle, and top object
            Duplicates them and uses commands from the 'stacker' module to create a stack
            Groups the pieces of the stack
        The first group created will be called 'stack001', the second 'stack002', etc
        Returns True if it completes without an error
        """
    def verify_args(self):
        """
        Accepts no arguments
        Checks the GUI to make sure it has all the information it needs
        If any of the arguments do not have a value:
            It calls 'warn_user' with an appropriate message
        It returns None
        Checks to make sure the user entered an integer for the number of stacks to make
            It calls 'warn_user' with an appropriate message
        It returns None
        If all of the arguments have a value which is valid, it returns True
        """
    def warn_user(self, title, message):
        """
        Accepts two arguments, a title and a message
        Displays a message box that locks the program till the user acknowledges it
        Use the code covered in the videos for this

        :param title: A title for the window
        :type: String
        :param message: A message to display in the window
        :type: String
        """
