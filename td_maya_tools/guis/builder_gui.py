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
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from PySide2 import QtGui, QtWidgets
from shiboken2 import wrapInstance
import random

# Imports That You Wrote
from td_maya_tools import stacker
from td_maya_tools import gen_utils

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
        Declares all the variables that will be necessary for the GUI to function

        :return: N/A
        """
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.main_vLayout = None
        self.top_lineEdit = None
        self.mid_lineEdit = None
        self.base_lineEdit = None
        self.stackAmt_lineEdit = None

    def init_gui(self):
        """
        Builds GUI window with the ability to set selected objects, modify text boxes,
        set the number of stacks, and create stacks.

        :return: N/A
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

    def make_options_layout(self):
        """
        Builds GUI window with the ability to set selected objects, modify text boxes,
        set the number of stacks, and create stacks.

        :return: QFormLayout
        """

    def set_selection(self):
        """
        Updates the appropriate line edit with the transform of the selection that was set

        :return: N/A
        """
        sender = self.sender()
        if sender:
            user_selection = cmds.ls(selection=True)
            if len(user_selection) < 1:
                return
            if sender.objectName() == 'button1':
                self.top_lineEdit.setText(', '.join(user_selection))
            if sender.objectName() == 'button2':
                self.mid_lineEdit.setText(', '.join(user_selection))
            if sender.objectName() == 'button3':
                self.base_lineEdit.setText(', '.join(user_selection))

    def make_stacks(self):
        """
        Verifies user input and creates stacks of objects

        :return: True if it completes without an error
        """
        # Return none if verification fails
        if self.verify_args() is None:
            return None

        # Create lists of object transforms from text boxes
        top_list = self.top_lineEdit.text().split(", ")
        mid_list = self.mid_lineEdit.text().split(", ")
        base_list = self.base_lineEdit.text().split(", ")
        stack_objs_list = []

        # Create specified number of stacks
        stacks_count = int(self.stackAmt_lineEdit.text())
        for index in range(1, stacks_count + 1):
            # Randomize top and base objects
            random.shuffle(top_list)
            stack_objs_list.append(top_list[0])
            random.shuffle(base_list)
            stack_objs_list.append(base_list[0])

            # Randomize middle objects based on max_height
            for i in range(self.max_height):
                random.shuffle(mid_list)
                stack_objs_list.append(mid_list[0])

            # Duplicate objects and move base to world origin
            transforms_list = []
            for obj in stack_objs_list:
                transforms_list.append(cmds.duplicate(top_list[0])[0])

            # Move the base object to the world origin, on top of the grid
            base_move = cmds.xform(transforms_list[0], boundingBox=True, query=True)
            cmds.move(0, -base_move[1], 0, transforms_list[0], relative=True)

            # Stack objects
            stacker.stack_objs(stack_objs_list)

            # Create group and place stacked objects in it
            stack_group = cmds.group(em=True, name="stack%s" % ("%03d" % index))
            for transform in transforms_list:
                cmds.parent(transform, stack_group)

        return True

    def verify_args(self):
        """
        Checks the GUI to make sure it has all the information it needs

        :return: None if verification fails, else True
        """
        top_list = []
        mid_list = []
        base_list = []
        error = ""

        # Create lists of object names if text box is not empty
        if len(self.top_lineEdit.text()) > 0:
            top_list = self.top_lineEdit.text().split(", ")
        if len(self.mid_lineEdit.text()) > 0:
            mid_list = self.mid_lineEdit.text().split(", ")
        if len(self.base_lineEdit.text()) > 0:
            base_list = self.base_lineEdit.text().split(", ")

        # Verify number and validity of top objects
        if len(top_list) < 1:
            error += "You must set a selection for the top parts.\n"
        else:
            for transform in top_list:
                if cmds.objExists(transform) is False:
                    error += "Top Stack transforms are invalid\n"

        # Verify number and validity of middle objects
        if len(mid_list) < 1:
            error += "You must set a selection for the mid parts.\n"
        else:
            for transform in mid_list:
                if cmds.objExists(transform) is False:
                    error += "Mid Stack transforms are invalid\n"

        # Verify number and validity of base objects
        if len(base_list) < 1:
            error += "You must set a selection for the base parts.\n"
        else:
            for transform in base_list:
                if cmds.objExists(transform) is False:
                    error += "Base Stack transforms are invalid\n"

        # Warn user if selection errors exist
        if error != "":
            self.warn_user('Builder - Selection', error)
            return None

        # Verify minimum stack number is met
        try:
            stack_amount = int(self.stackAmt_lineEdit.text())
            if stack_amount < 1:
                error += "Must have at least 1 stack\n"
        # Verify that stack input is an integer
        except ValueError:
            if self.stackAmt_lineEdit.text() is None:
                error += "You must specify the number of buildings to make"
            else:
                error += "The value for the number of buildings must be an integer\n"

        # Warn user if count errors exist
        if error != "":
            self.warn_user('Builder - Count', error)
            return None

        return True

    def add_stack_to_tree_view(self, stack_node, contents_list):
        """
        Builds GUI window with the ability to set selected objects, modify text boxes,
        set the number of stacks, and create stacks.

        :param stack_node: The name of a group node, e.g. 'stack001'
        :type: str

        :param contents_list: A list of the contents of that group (the stack node)
        :type: list of ???

        :return: N/A
        """
        # Add the group name to the tree
        # Nest the transform nodes under the tree
        # Clicking on an item in the tree view selects that item in maya

    @classmethod
    def apply_xml(cls):
        """
        Allows the user to select an XML file and applies the values of the file to the
        stacks in the scene.

        :return: None if an invalid file is selected, else True
        """
        # Prompt the user to select a file
        filename, ffilter = QtWidgets.QFileDialog.getOpenFileName(caption='Open File',
                                                                  dir='C:/Users/',
                                                                  filter='Text Files ('
                                                                        '*.txt)')
        if not filename:
            return None

        # Checks to see that the dictionary has some values
        xml_data = gen_utils.read_stack_xml(filename)
        if not xml_data:
            return None
        stacks = xml_data['maya_stacks'].keys()
        for stack in stacks:
            # Apply values to the stacks in scene
            for transform in xml_data['maya_stacks'][stack]:
                # FIXME Incorrect data probably
                # print(xml_data['maya_stacks'][stack][transform] + " " + transform)
                cmds.move(xml_data['maya_stacks'][stack][transform], transform)

        # root = 'stacks'
        # maya_stacks
            # stack001
                # tx value="2"
                # ty value="0"
                # tz value="3"
            # stack002 ...

    def tree_item_clicked(self):
        """
        Can accept up to two arguments depending on the logic you use.
        Feel free to use the example from class or another method available on the tree
        view widget.

        :return: None if an invalid file is selected, else True
        """

    # noinspection PyMethodMayBeStatic
    def warn_user(self, title, message):
        """
        Displays a message box that locks the program till the user acknowledges it

        :param title: A title for the window
        :type: String

        :param message: A message to display in the window
        :type: String

        :return: N/A
        """
        # Create warning dialog
        cmds.confirmDialog(title=title,
                           message=message,
                           button='OK',
                           icon="warning")
