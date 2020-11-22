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
import td_maya_tools.stacker as stacker

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
        self.optLayout = None
        self.top_lineEdit = None
        self.mid_lineEdit = None
        self.base_lineEdit = None
        self.stack_lineEdit = None
        self.height_lineEdit = None
        self.offset_lineEdit = None
        
    def init_gui(self):
        """
        Builds GUI window with the ability to set selected objects, modify text boxes,
        set the number of stacks, and create stacks.

        Calls make_options_layout to get the options layout portion of the GUI.
        Adds a tree view widget that tracks the stack groups that are added.
            The tree view entries are set-up such that the name of the transforms nodes
            are under the group name.
            Clicking on something in the tree view calls tree_item_clicked

        :return: N/A
        """

        # Create the main layout (Vertical)
        #self.main_vLayout = QtWidgets.QVBoxLayout(self)

        # Create the QFormLayout
        self.optLayout = QtWidgets.QFormLayout(self)

        # Create the row layouts
        top_hLayout = QtWidgets.QHBoxLayout()
        mid_hLayout = QtWidgets.QHBoxLayout()
        base_hLayout = QtWidgets.QHBoxLayout()
        stack_hLayout = QtWidgets.QHBoxLayout()
        height_hLayout = QtWidgets.QHBoxLayout()
        offset_hLayout = QtWidgets.QHBoxLayout()

        # Add the row layouts to the main layout
        self.optLayout.addRow(top_hLayout)
        self.optLayout.addRow(mid_hLayout)
        self.optLayout.addRow(base_hLayout)
        self.optLayout.addRow(stack_hLayout)
        self.optLayout.addRow(height_hLayout)
        self.optLayout.addRow(offset_hLayout)

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
        stack_label = QtWidgets.QLabel('Set Stack Count')
        self.stack_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control


        # Add the buttons / line edits to the a new row
        stack_hLayout.addWidget(stack_label)
        stack_hLayout.addWidget(self.stack_lineEdit)

        # A label and a line edit that allows the user to specify the max height
        height_label = QtWidgets.QLabel('Set Max Height')
        self.height_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the height amount control


        # Add the buttons / line edits to the a new row
        height_hLayout.addWidget(height_label)
        height_hLayout.addWidget(self.height_lineEdit)

        # A label and a line edit that allows the user to specify the separation
        offset_label = QtWidgets.QLabel('Set Separation')
        self.offset_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control


        # Add the buttons / line edits to the a new row
        offset_hLayout.addWidget(offset_label)
        offset_hLayout.addWidget(self.offset_lineEdit)

        # A horizontal layout to hold the 'Load XML', 'Make Stacks', and 'Cancel' buttons
        buttons_hLayout = QtWidgets.QHBoxLayout()
        self.optLayout.addRow(buttons_hLayout)

        # A 'Load XML' button to load the XML file by calling 'apply_xml'
        xml_button = QtWidgets.QPushButton('Load XML')
        xml_button.setStyleSheet("background-color: orange")
        xml_button.clicked.connect(self.make_stacks)

        # A 'Make Stacks' button to make each stack by calling 'make_stacks'
        stack_button = QtWidgets.QPushButton('Make Stacks')
        stack_button.setStyleSheet("background-color: green")
        stack_button.clicked.connect(self.make_stacks)

        # A 'Cancel' button, which calls 'self.close' to close the GUI
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.setStyleSheet("background-color: IndianRed")
        cancel_button.clicked.connect(self.close)

        # Add the buttons to the button row
        buttons_hLayout.addWidget(xml_button)
        buttons_hLayout.addWidget(stack_button)
        buttons_hLayout.addWidget(cancel_button)

        # Configure the window
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('Builder')
        self.show()

    def make_options_layout(self):
        """
        Uses a QFormLayout to place the different widgets, which will include:
        Three buttons that set the selection for the top, middle, and bottom parts.
        Three un-editable line edits that acknowledge that top, middle, and bottom parts
        have been set.
            They do this by showing the number of items and coloring the background a
            green color.
        Three labels that indicate the stack count, max, height, and separation values.
        A QSpinBox that allows the user to enter a count, with a default value of 3.
        A QSpinBox that allows the user to enter a max height from 1 to 6, with a default
        of 3.
        A QDoubleSpinBox that allows the user to set a separation value in .1 increments,
        default value of .1

        :return: QFormLayout
        """

        # Create the QFormLayout
        self.optLayout = QtWidgets.QVBoxLayout(self)

        # Create the three row layouts (Horizontal)
        top_hLayout = QtWidgets.QHBoxLayout()
        mid_hLayout = QtWidgets.QHBoxLayout()
        base_hLayout = QtWidgets.QHBoxLayout()
        # Add the row layouts to the main layout
        self.optLayout.addLayout(top_hLayout)
        self.optLayout.addLayout(mid_hLayout)
        self.optLayout.addLayout(base_hLayout)

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
        stack_label = QtWidgets.QLabel('Set Stack Count')
        self.stack_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control
        stack_hLayout = QtWidgets.QHBoxLayout()
        self.optLayout.addLayout(stack_hLayout)
        # Add the buttons / line edits to the a new row
        stack_hLayout.addWidget(stack_label)
        stack_hLayout.addWidget(self.stack_lineEdit)

        # A label and a line edit that allows the user to specify the max height
        height_label = QtWidgets.QLabel('Set Max Height')
        self.height_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the height amount control
        height_hLayout = QtWidgets.QHBoxLayout()
        self.optLayout.addLayout(height_hLayout)
        # Add the buttons / line edits to the a new row
        height_hLayout.addWidget(height_label)
        height_hLayout.addWidget(self.height_lineEdit)

        # A label and a line edit that allows the user to specify the separation
        offset_label = QtWidgets.QLabel('Set Separation')
        self.offset_lineEdit = QtWidgets.QLineEdit()
        # Create a new row to hold the stack amount control
        offset_hLayout = QtWidgets.QHBoxLayout()
        self.optLayout.addLayout(offset_hLayout)
        # Add the buttons / line edits to the a new row
        offset_hLayout.addWidget(offset_label)
        offset_hLayout.addWidget(self.offset_lineEdit)

        # A horizontal layout to hold the 'Load XML', 'Make Stacks', and 'Cancel' buttons
        buttons_hLayout = QtWidgets.QHBoxLayout()
        self.optLayout.addLayout(buttons_hLayout)

        # A 'Load XML' button to load the XML file by calling 'apply_xml'
        xml_button = QtWidgets.QPushButton('Load XML')
        xml_button.setStyleSheet("background-color: orange")
        xml_button.clicked.connect(self.make_stacks)

        # A 'Make Stacks' button to make each stack by calling 'make_stacks'
        stack_button = QtWidgets.QPushButton('Make Stacks')
        stack_button.setStyleSheet("background-color: green")
        stack_button.clicked.connect(self.make_stacks)

        # A 'Cancel' button, which calls 'self.close' to close the GUI
        cancel_button = QtWidgets.QPushButton('Cancel')
        cancel_button.setStyleSheet("background-color: IndianRed")
        cancel_button.clicked.connect(self.close)

        # Add the buttons to the button row
        buttons_hLayout.addWidget(xml_button)
        buttons_hLayout.addWidget(stack_button)
        buttons_hLayout.addWidget(cancel_button)

        return self.optLayout

    def set_selection(self):
        """
        Updates the appropriate line edit with the count of objects in the set selection

        Updated to show a count of objects instead of names.
        Updated to show a green color in the background once the user sets a valid
        selection.

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

        Calls 'verify_args' to make sure the user has entered all the information it will
        need.
                If a None value is returned from 'verify_args', then this method
                immediately returns a None value too.
            Uses a for loop to create the stacks, based on the value of the count spin box
                Uses the 'random' Python library to pick a base object and duplicates it.
                Adds a nested for loop to decide how many random mid objects to add, based
                on the height spin box.
                    Uses random for each mid object so they can be different.
                    Duplicates all the objects it needs.
                Uses random to pick a top object and duplicates it.
                The duplicated objects are used to make a stack using logic from the
                stacker module.
                Groups the pieces of the stack, with the base object sitting on the grid,
                and its pivot at the origin.
        The first group created will be called 'stack001', the second 'stack002', etc.
        Adds the group and its contents to the tree view by calling add_stack_to_tree_view
        Adding all the newly created items in a list for each iteration of the loop makes
        this easier.
        Offsets the groups by the amount from the separation spin box using the
        offset_objs_in_x function.
            Using a for loop that iterates over the stack groups will make this part
            simple.
            If all of the groups nodes are added to another list as they are created
            you'll have them available here.
            Returns True if it completes without an error.


        :return: True if it completes without an error
        """
        # Return none if verification fails
        if self.verify_args() is None:
            return None

        # Create lists of object transforms from text boxes
        top_list = self.top_lineEdit.text().split(", ")
        mid_list = self.mid_lineEdit.text().split(", ")
        base_list = self.base_lineEdit.text().split(", ")

        try:
            # Create specified number of stacks
            for index in range(1, int(self.stackAmt_lineEdit.text()) + 1):
                # Randomize top, middle, and base objects
                random.shuffle(top_list)
                random.shuffle(mid_list)
                random.shuffle(base_list)

                # Duplicate objects and move base to world origin
                base_transform = cmds.duplicate(base_list[0])[0]
                mid_transform = cmds.duplicate(mid_list[0])[0]
                top_transform = cmds.duplicate(top_list[0])[0]

                # Center the base object to the world origin
                cmds.move(0, 0, 0, base_transform, absolute=True)

                # Stack objects
                stacker.stack_objs([base_transform, mid_transform, top_transform])

                # Create and empty group and parent the stacked objects to it
                stack_group = cmds.group(em=True, name="stack%s" % ("%03d" % index))
                cmds.parent(base_transform, stack_group)
                cmds.parent(mid_transform, stack_group)
                cmds.parent(top_transform, stack_group)
        except RuntimeError:
            # Return None if an error occurs
            return None

        return True

    def verify_args(self):
        """
        Checks the GUI to make sure it has all the information it needs

        Accepts no arguments.
        The base, mid, and top parts must have a valid selection set.
        Updated to check the three new spin boxes.
            The stack count has to be at least 1.
            The max height can be any value from 1 to 6.
            The separation value must be at least 0.1.
            If any of the arguments do not have a value:
                It calls 'warn_user' with an appropriate message.
        It returns None.
            Returns True if all of the arguments have a valid value.


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

    def add_stack_to_tree_view(self):
        """
        Accepts two arguments:
            The name of a group node, e.g. 'stack001'
            A list of the contents of that group (the transform nodes).
        Called from the make_stacks method.
        Adds the group name to the tree and nests the transform nodes under it.
        It holds all of the groups created by the tool.
        Clicking on an item in the tree view selects that item in Maya.

        :return:
        """

    def apply_xml(self):
        """
        Allows the user to select an XML file and applies the values of the file to the
        stacks in the scene.

        :return: None if an invalid file is selected, else True
        """

    def tree_item_clicked(self):
        """
        Can accept up to two arguments depending on the logic you use.
        Feel free to use the example from class or another method available on the tree
        view widget.

        :return:
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
