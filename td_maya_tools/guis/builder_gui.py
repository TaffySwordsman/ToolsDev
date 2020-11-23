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
        self.main_hLayout = None
        self.optLayout = None
        self.top_lineEdit = None
        self.mid_lineEdit = None
        self.base_lineEdit = None
        self.top_objs = None
        self.mid_objs = None
        self.base_objs = None
        self.stack_box = None
        self.height_box = None
        self.offset_box = None
        
    def init_gui(self):
        """
        Builds GUI window with the ability to set selected objects, set stack size,
        height, and separation values, load XML files, and create stacks.

        :return: N/A
        """
        # Create the main layouts (Vertical & Horizontal)
        self.main_vLayout = QtWidgets.QVBoxLayout(self)
        self.main_hLayout = QtWidgets.QHBoxLayout(self)

        # Call make_options_layout to get the options layout portion of the GUI.
        self.main_hLayout.addLayout(self.make_options_layout())

        # Add tree view widget that tracks added stack groups
        tree_view = QtWidgets.QTreeWidget()
        tree_view.setHeaderLabel('Object Stacks')
        self.main_hLayout.addWidget(tree_view)

        # Add widgets to horizontal layout
        self.main_vLayout.addLayout(self.main_hLayout)

        # A horizontal layout to hold the 'Load XML', 'Make Stacks', and 'Cancel' buttons
        buttons_hLayout = QtWidgets.QHBoxLayout()
        self.main_vLayout.addLayout(buttons_hLayout)

        # A 'Load XML' button to load the XML file by calling 'apply_xml'
        xml_button = QtWidgets.QPushButton('Load XML')
        xml_button.setStyleSheet("background-color: DarkOrange")
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
        self.setGeometry(300, 300, 450, 250)
        self.setWindowTitle('Builder')
        self.show()

    def make_options_layout(self):
        """
        Uses a QFormLayout to place the different widgets including 3 buttons that set
        the selection for the top, middle, and bottom parts, 3 uneditable line edits that
        acknowledge when the top, middle, and bottom parts have been set, 3 labels
        indicating the stack count, max height, and separation values, and 3 spin boxes
        which allow the user to set the values for the stack count, max height, and
        separation values.

        :return: QFormLayout
        """
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

        # Disable line edits
        self.top_lineEdit.setEnabled(False)
        self.mid_lineEdit.setEnabled(False)
        self.base_lineEdit.setEnabled(False)

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

        # A label and a spin box that allows the user to specify how many stacks to make
        stack_label = QtWidgets.QLabel('Set Stack Count')
        self.stack_box = QtWidgets.QSpinBox()
        self.stack_box.setValue(3)

        # Add the label / spin box to a new row
        stack_hLayout.addWidget(stack_label)
        stack_hLayout.addWidget(self.stack_box)
        self.stack_box.setValue(3)

        # A label and a spin box that allows the user to specify the max height
        height_label = QtWidgets.QLabel('Set Max Height')
        self.height_box = QtWidgets.QSpinBox()
        self.height_box.setValue(3)
        self.height_box.setMinimum(1)
        self.height_box.setMaximum(6)

        # Add the label / spin box to the a new row
        height_hLayout.addWidget(height_label)
        height_hLayout.addWidget(self.height_box)

        # A label and a double spin box that allows the user to specify the separation
        offset_label = QtWidgets.QLabel('Set Separation')
        self.offset_box = QtWidgets.QDoubleSpinBox()
        self.offset_box.setValue(0.1)
        self.offset_box.setSingleStep(0.1)

        # Add the label / double spin box to the a new row
        offset_hLayout.addWidget(offset_label)
        offset_hLayout.addWidget(self.offset_box)

        return self.optLayout

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
            numObjs = str(len(user_selection)) + " objects"
            if sender.objectName() == 'button1':
                self.top_objs = user_selection
                self.top_lineEdit.setText(numObjs)
                self.top_lineEdit.setStyleSheet(
                    "background-color: DarkOliveGreen; color: white")
            if sender.objectName() == 'button2':
                self.mid_objs = user_selection
                self.mid_lineEdit.setText(numObjs)
                self.mid_lineEdit.setStyleSheet(
                    "background-color: DarkOliveGreen; color: white")
            if sender.objectName() == 'button3':
                self.base_objs = user_selection
                self.base_lineEdit.setText(numObjs)
                self.base_lineEdit.setStyleSheet(
                    "background-color: DarkOliveGreen; color: white")

    def make_stacks(self):
        """
        Verifies user input and creates stacks of objects

        :return: True if it completes without an error
        """
        # Return none if verification fails
        if self.verify_args() is None:
            return None

        # Create lists of object transforms from text boxes
        top_list = self.top_objs
        mid_list = self.mid_objs
        base_list = self.base_objs
        stack_objs_list = []

        # Create specified number of stacks
        stacks_count = int(self.stack_box.text())
        for index in range(1, stacks_count + 1):
            # Randomize top and base objects
            random.shuffle(top_list)
            stack_objs_list.append(top_list[0])
            random.shuffle(base_list)
            stack_objs_list.append(base_list[0])

            # Randomize middle objects based on max_height
            for i in range(self.height_box.value()):
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
            self.add_stack_to_tree_view(stack_group)

        return True

    def verify_args(self):
        """
        Checks the GUI to make sure it has all the information it needs

        :return: None if verification fails, else True
        """
        error = ""

        # Verify number and validity of top objects
        if len(self.top_objs) < 1:
            error += "You must set a selection for the top parts.\n"
        else:
            for transform in self.top_objs:
                if cmds.objExists(transform) is False:
                    error += "Top Stack transforms are invalid\n"

        # Verify number and validity of middle objects
        if len(self.mid_objs) < 1:
            error += "You must set a selection for the mid parts.\n"
        else:
            for transform in self.mid_objs:
                if cmds.objExists(transform) is False:
                    error += "Mid Stack transforms are invalid\n"

        # Verify number and validity of base objects
        if len(self.base_objs) < 1:
            error += "You must set a selection for the base parts.\n"
        else:
            for transform in self.base_objs:
                if cmds.objExists(transform) is False:
                    error += "Base Stack transforms are invalid\n"

        # Warn user if selection errors exist
        if error != "":
            self.warn_user('Builder - Selection', error)
            return None

        # Verify minimum stack number is met
        stack_amount = int(self.stack_box.text())
        if stack_amount < 1:
            self.warn_user('Builder - Count',"You must make at least one stack")
            return None

        # Verify minimum height number is met
        stack_amount = int(self.height_box.value())
        if stack_amount < 3 or stack_amount > 6:
            self.warn_user('Builder - Height', "The height must be a value from 3 to 6")
            return None

        # Verify minimum separation number is valid
        stack_amount = int(self.offset_box.value())
        if stack_amount <= 0:
            self.warn_user('Builder - Distance', "The distance must be greater than 0.00")
            return None

        return True

    def add_stack_to_tree_view(self, stack_node, contents_list):
        """
        Builds GUI window with the ability to set selected objects, modify text boxes,
        set the number of stacks, and create stacks.

        :param stack_node: The name of a group node, e.g. 'stack001'
        :type: str

        :param contents_list: A list of the contents of that group (the stack node)
        :type: list of transforms

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
