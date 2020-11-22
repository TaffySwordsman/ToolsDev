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
    A tool that stacks random shapes on top of each other.

:description:
    This module takes 3 named objects, finds the top and bottom center points of each,
    and stacks each one on top of the other by moving them a relative distance from their
    bottom center point to the top center point of the previous object.

:applications:
    Maya

:see_also:
    N/A
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds

# Imports That You Wrote
# N/A

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


def offset_objs_in_x(obj1, obj2, offset):
    """
    This function moves the objects by the offset amount

	:param obj1: The transform node of an object that will not be moved.
	:type: str

	:param obj2: The transform node of an object that will be moved.
	:type: str

	:param offset: The amount of offset in 'x' that should be between the bounding boxes
	of the two objects.
	:type: double

	:return: N/A
    """

    # Uses the xform command to get the bounding boxes of the two objects passed in.
    # Moves the second object along the 'x' axis.
    # The corresponding bounding box edges are separated by the value provided.
    # Reference the video to see how this looks.


def stack_objs(obj_list):
    """
    This function stacks 3 named objects one on top of the other.

    :param obj_list: The name of the transform nodes to be stacked
    :type: list of strings

    :return: Success of stacking objects
    :type: bool
    """

    # Get result of verifying arguments
    verification = verify_args(obj_list)

    # If verification failed, error is printed and script returns None
    if verification is None:
        print("Incorrect arguments given")
        return None

    try:
        for index in range(len(obj_list) - 1):
            # Gets top center of mid and bottom center of top objects
            moving_obj = obj_list[index + 1]
            moving_obj_center = get_center_point(obj_list[index + 1], bottom=True)
            base_obj_center = get_center_point(obj_list[index], top=True)

            # Move the top object so it is resting on the mid object
            create_stack(moving_obj, moving_obj_center, base_obj_center)
    except RuntimeError:
        # Return None if an error occurs
        return None

    # Return True
    return True


def create_stack(obj_name, transform_from, transform_to):
    """
    This function calculates relative distance between two points and moves the object
    that relative distance.

    :param obj_name: The name of the transform node to move.
    :type: str

    :param transform_from: The bottom center of the object to move
    :type: list of transform values (x, y, z)

    :param transform_to: The top center of the object that will not move
    :type: list of transform values (x, y, z)

    :return: N/A
    """

    # Calculate x, y, and z coordinates to move to
    x_move = transform_to[0] - transform_from[0]
    y_move = transform_to[1] - transform_from[1]
    z_move = transform_to[2] - transform_from[2]

    # Move object
    cmds.move(x_move, y_move, z_move, obj_name, relative=True)


def get_center_point(obj_name, top=False, bottom=False):
    """
    This function gets the bounding box of an object and returns the top center or bottom
    center x y z coordinates depending on the selected flag.

    :param obj_name: The name of the base transform node.
    :type: str

    :param top: A flag that indicates if it is getting the top center. (Def=False)
    :type: bool

    :param bottom: A flag that indicates if it is getting the bottom center. (Def=False)
    :type: bool

    :return: A list with the top/bottom center coordinates based on flag.
    :type: list
    """

    # Get list of values from bounding box
    bounding_box = cmds.xform(obj_name, boundingBox=True, query=True)

    # If top, calculate x and z averages then return top center coordinates
    if top:
        x = (bounding_box[0] + bounding_box[3]) / 2
        y = bounding_box[4]
        z = (bounding_box[2] + bounding_box[5]) / 2
        return [x, y, z]

    # If bottom, calculate x and z averages then return bottom center coordinates
    if bottom:
        x = (bounding_box[0] + bounding_box[3]) / 2
        y = bounding_box[1]
        z = (bounding_box[2] + bounding_box[5]) / 2
        return [x, y, z]


def verify_args(obj_list):
    """
    This function verifies the names of 3 transform nodes and returns the result

    :param obj_list: The name of the transform nodes.
    :type: list of strings

    :return: Whether or not any/all of the arguments have a value.
    :type: bool
    """

    for obj in obj_list:
        exists = cmds.objExists
        if not exists:
            # If one or more arguments don't have a value return None
            return None

    # If all of the arguments have a value return True
    return True


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
