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
import maya.cmds as cmds
import random

# Imports That You Wrote
import td_maya_tools.stacker

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


class BuilderGUI(QtWidgets.QDialog):
    def __init__(self):
        """
        Accepts no arguments
        Declares all the variables that will be necessary for the GUI to function
        """
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.main_vLayout = None
        self.top_lineEdit = None
        self.mid_lineEdit = None
        self.base_lineEdit = None
        self.stackAmt_lineEdit = None
        self.top_list = []
        self.mid_list = []
        self.base_list = []

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
        # Create the main layout (Vertical)
        self.main_vLayout = QtWidgets.QVBoxLayout(self)

        # Create the three row layouts (Horizontal)
        top_hLayout = QtWidgets.QHBoxLayout()
        mid_hLayout = QtWidgets.QHBoxLayout()
        base_hLayout = QtWidgets.QHBoxLayout()
        # Add the row layouts to the main layout
        self.main_vLayout.addLayout(top_hLayout)
        self.main_vLayout.addLayout(mid_hLayout)
        self.main_vLayout.addLayout(base_hLayout)

        # Create the buttons and line edits
        button1 = QtWidgets.QPushButton('Set Top Parts')
        button2 = QtWidgets.QPushButton('Set Mid Parts')
        button3 = QtWidgets.QPushButton('Set Base Parts')
        self.top_lineEdit = QtWidgets.QLineEdit()
        self.mid_lineEdit = QtWidgets.QLineEdit()
        self.base_lineEdit = QtWidgets.QLineEdit()
        # Name the buttons
        button1.setObjectName('button1')
        button2.setObjectName('button2')
        button3.setObjectName('button3')
        # Connect the buttons to 'Set Selection'
        button1.clicked.connect(self.set_selection)
        button2.clicked.connect(self.set_selection)
        button3.clicked.connect(self.set_selection)
        # Add the buttons and line edits to the rows
        top_hLayout.addWidget(button1)
        top_hLayout.addWidget(self.top_lineEdit)
        mid_hLayout.addWidget(button2)
        mid_hLayout.addWidget(self.mid_lineEdit)
        base_hLayout.addWidget(button3)
        base_hLayout.addWidget(self.base_lineEdit)

        # A label and a line edit that allows the user to specify how many stacks to make
        stackAmt_label = QtWidgets.QLabel('Number of Stacks to Make:')
        self.stackAmt_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control
        stackAmt_hLayout = QtWidgets.QHBoxLayout()
        self.main_vLayout.addLayout(stackAmt_hLayout)
        # Add the buttons / line edits to the a new row
        stackAmt_hLayout.addWidget(stackAmt_label)
        stackAmt_hLayout.addWidget(self.stackAmt_lineEdit)

        # A horizontal layout to hold the 'Make Stacks' and 'Cancel' buttons
        buttons_hLayout = QtWidgets.QHBoxLayout()
        self.main_vLayout.addLayout(buttons_hLayout)
        # A 'Make Stacks' button to make each stack by calling 'make_stacks'
        stack_button = QtWidgets.QPushButton('Make Stacks')
        stack_button.clicked.connect(self.make_stacks)
        # A 'Cancel' button, which calls 'self.close' to close the GUI
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        # Add the two buttons to the button row
        buttons_hLayout.addWidget(stack_button)
        buttons_hLayout.addWidget(cancel_button)

        # Configure the window
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Builder')
        self.show()

    def set_selection(self):
        """
        Accepts no arguments
        Uses the sender to determine which button called it
        Updates the appropriate line edit with the transform of the selection that was set
        """
        sender = self.sender()
        if sender:
            user_selection = cmds.ls(selection=True)
            if len(user_selection) < 1:
                return
            if sender.objectName() == 'button1':
                self.top_list = user_selection
                self.top_lineEdit.setText(', '.join(user_selection))
            if sender.objectName() == 'button2':
                self.mid_list = user_selection
                self.mid_lineEdit.setText(', '.join(user_selection))
            if sender.objectName() == 'button3':
                self.base_list = user_selection
                self.base_lineEdit.setText(', '.join(user_selection))

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
        if self.verify_args() is None:
            return None
        for index in range(1, int(self.stackAmt_lineEdit.text()) + 1):
            random.shuffle(self.top_list)
            random.shuffle(self.mid_list)
            random.shuffle(self.base_list)
            top_transform = cmds.duplicate(self.top_list[0])[0]
            mid_transform = cmds.duplicate(self.mid_list[0])[0]
            base_transform = cmds.duplicate(self.base_list[0])[0]
            stack_group = cmds.group(em=True, name="stack%s" % ("%03d" % index))
            cmds.parent(top_transform, stack_group)
            cmds.parent(mid_transform, stack_group)
            cmds.parent(base_transform, stack_group)
            td_maya_tools.stacker.stack_objs(top_transform, mid_transform, base_transform)
        return True

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
        :return: None
        """
        error = ""
        if len(self.top_list) < 1:
            error += "Must have a valid top stack\n"
        else:
            for transform in self.top_list:
                if cmds.objExists(transform) is False:
                    error += "Top Stack transforms are invalid\n"
        if len(self.mid_list) < 1:
            error += "Must have a valid mid stack\n"
        else:
            for transform in self.mid_list:
                if cmds.objExists(transform) is False:
                    error += "Mid Stack transforms are invalid\n"
        if len(self.base_list) < 1:
            error += "Must have a valid base stack\n"
        else:
            for transform in self.base_list:
                if cmds.objExists(transform) is False:
                    error += "Base Stack transforms are invalid\n"
        try:
            stack_amount = int(self.stackAmt_lineEdit.text())
            if stack_amount < 1:
                return None
        except ValueError:
            error += "Must have a valid stack amount\n"
        if error != "":
            self.warn_user('Warning', error)
            return None
        return True

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
        cmds.confirmDialog(title=title,
                           message=message,
                           button='OK')
