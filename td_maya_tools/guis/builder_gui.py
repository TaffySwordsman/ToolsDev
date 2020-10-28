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
        self.lineEdit1 = None
        self.lineEdit2 = None
        self.lineEdit3 = None
        self.lineEdit_stackAmt = None

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
        row1_hLayout = QtWidgets.QHBoxLayout()
        row2_hLayout = QtWidgets.QHBoxLayout()
        row3_hLayout = QtWidgets.QHBoxLayout()
        # Add the row layouts to the main layout
        self.main_vLayout.addLayout(row1_hLayout)
        self.main_vLayout.addLayout(row2_hLayout)
        self.main_vLayout.addLayout(row3_hLayout)

        # Create the buttons and line edits
        button1 = QtWidgets.QPushButton('Set Selection')
        button2 = QtWidgets.QPushButton('Set Selection')
        button3 = QtWidgets.QPushButton('Set Selection')
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.lineEdit3 = QtWidgets.QLineEdit()
        # Name the buttons
        button1.setObjectName('button1')
        button2.setObjectName('button2')
        button3.setObjectName('button3')
        # Connect the buttons to 'Set Selection'
        button1.clicked.connect(self.set_selection)
        button2.clicked.connect(self.set_selection)
        button3.clicked.connect(self.set_selection)
        # Add the buttons and line edits to the rows
        row1_hLayout.addWidget(self.lineEdit1)
        row1_hLayout.addWidget(button1)
        row2_hLayout.addWidget(self.lineEdit2)
        row2_hLayout.addWidget(button2)
        row3_hLayout.addWidget(self.lineEdit3)
        row3_hLayout.addWidget(button3)

        # A label and a line edit that allows the user to specify how many stacks to make
        label_stackAmt = QtWidgets.QLabel('Stack Amount')
        self.lineEdit_stackAmt = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control
        stackRow_hLayout = QtWidgets.QHBoxLayout()
        self.main_vLayout.addLayout(stackRow_hLayout)
        # Add the buttons / line edits to the a new row
        stackRow_hLayout.addWidget(label_stackAmt)
        stackRow_hLayout.addWidget(self.lineEdit_stackAmt)

        # A 'Make Stacks' button to make each stack by calling 'make_stacks'
        button_stack = QtWidgets.QPushButton('Make Stacks')
        button_stack.clicked.connect(self.make_stacks)
        # Add the buttons / line edits to the middle row
        self.main_vLayout.addWidget(button_stack)

        # A 'Cancel' button, which calls 'self.close' to close the GUI
        button_cancel = QtWidgets.QPushButton('Cancel')
        button_cancel.clicked.connect(self.close)
        # Add the buttons / line edits to the bottom row
        self.main_vLayout.addWidget(button_cancel)

        # Configure the window
        self.setGeometry(300, 300, 250, 450)
        self.setWindowTitle('Stack Builder')
        self.show()

    def set_selection(self):
        """
        Accepts no arguments
        Uses the sender to determine which button called it
        Updates the appropriate line edit with the transform of the selection that was set
        """
        sender = self.sender()
        if sender:
            user_selection = cmds.ls(selection=True, tail=1)
            if len(user_selection) < 1:
                return
            if sender.objectName() == 'button1':
                self.lineEdit1.setText(user_selection[0])
            if sender.objectName() == 'button2':
                self.lineEdit2.setText(user_selection[0])
            if sender.objectName() == 'button3':
                self.lineEdit3.setText(user_selection[0])

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
        orig_list = [self.lineEdit1.text(), self.lineEdit2.text(), self.lineEdit3.text()]
        for index in range(1, int(self.lineEdit_stackAmt.text()) + 1):
            random.shuffle(orig_list)
            stack_group = cmds.group(em=True, name="stack%s" % ("%03d" % index))
            stack_list = []
            for transform in orig_list:
                new_transform = cmds.duplicate(transform)[0]
                cmds.parent(new_transform, stack_group)
                stack_list.append(new_transform)
            td_maya_tools.stacker.stack_objs(stack_list[0], stack_list[1], stack_list[2])
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
        transforms = [self.lineEdit1.text(), self.lineEdit2.text(), self.lineEdit3.text()]
        for transform in transforms:
            if transform is None or transform == '':
                self.warn_user('Warning', "Every transform must contain a valid object")
                return None
            if cmds.objExists(transform) is False:
                self.warn_user('Warning', "Every transform must contain a valid object")
                return None
        try:
            stack_amount = int(self.lineEdit_stackAmt.text())
            if stack_amount < 1:
                self.warn_user('Warning', "Must have a valid stack amount")
                return None
        except ValueError:
            self.warn_user('Warning', "Must have a valid stack amount")
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
        print("%s: %s" % (title, message))
