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


def stack_objs(base_name, mid_name, top_name):
    """
    This function stacks 3 named objects one on top of the other.

    :param base_name: The name of the base transform node.
    :type: str

    :param mid_name: The name of the mid transform node.
    :type: str

    :param top_name: The name of the top transform node.
    :type: str

    :return: Success of stacking objects
    :type: bool
    """

    # Get result of verifying arguments
    verification = verify_args(base_name, mid_name, top_name)

    # If verification failed, error is printed and script returns None
    if verification is None:
        print("Incorrect arguments given")
        return None

    # Get top center of base and bottom center of mid objects
    base_center_top = get_center_point(base_name, top=True)
    mid_center_bottom = get_center_point(mid_name, bottom=True)

    # Move the mid object so it is resting on the base object
    create_stack(mid_name, mid_center_bottom, base_center_top)

    # Gets top center of mid and bottom center of top objects
    mid_center_top = get_center_point(mid_name, top=True)
    top_center_bottom = get_center_point(top_name, bottom=True)

    # Move the top object so it is resting on the mid object
    create_stack(top_name, top_center_bottom, mid_center_top)

    # Return True
    return True


def create_stack(obj_name, transform_from, transform_to):
    """
    This function calculates relative distance between two points and moves the object
    that relative distance.

    :param obj_name: The name of the base transform node.
    :type: str

    :param transform_from: The bottom center of the object to move (x,y,z values).
    :type: transform

    :param transform_to: The point in space to place the object (x,y,z values).
    :type: transform

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


def verify_args(base_name, mid_name, top_name):
    """
    This function verifies the names of 3 transform nodes and returns the result

    :param base_name: The name of the base transform node.
    :type: str

    :param mid_name: The name of the mid transform node.
    :type: str

    :param top_name: The name of the top transform node.
    :type: str

    :return: Whether or not any/all of the arguments have a value.
    :type: bool
    """

    base_exists = cmds.objExists(base_name)
    mid_exists = cmds.objExists(mid_name)
    top_exists = cmds.objExists(top_name)

    # If all of the arguments have a value return True
    if base_exists and mid_exists and top_exists:
        return True

    # If one or more arguments don't have a value return None
    return None


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
