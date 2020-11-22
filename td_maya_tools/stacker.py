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
    This module takes a list of named objects, finds the top and bottom center points of
    each, and stacks each one on top of the other by moving them a relative distance from
    their bottom center point to the top center point of the previous object.

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


def offset_objs_in_x(static_name, moved_name, offset):
    """
    This function offsets one object by 'x' amount from another one.

    :param static_name: The transform node of an object that will not be moved.
    :type: str

    :param moved_name: The transform node of an object that will be moved.
    :type: str

    :param offset: The amount of offset in 'x' that should be between the bounding boxes
    of the two objects.
    :type: float

    :return: N/A
    """

    # Get the bounding boxes of the two objects passed in.
    bb_static = cmds.xform(static_name, boundingBox=True, query=True)
    bb_moved = cmds.xform(moved_name, boundingBox=True, query=True)

    # Calculate position to move object
    x_move = bb_static[3] + offset + abs((bb_moved[3] - bb_moved[0]) / 2)

    # Move object along x-axis
    cmds.move(x_move, 0, 0, moved_name, moveX=True)


def stack_objs(objects):
    """
    This function stacks a list of named objects one on top of the other according to
    their order in the list.

    :param objects: A list containing all the objects to be stacked.
    :type: list of strings
    
    :return: Success of stacking objects
    :type: bool
    """

    # Get result of verifying arguments
    verification = verify_args(objects)

    # If verification failed, error is printed and script returns None
    if verification is None:
        print("Incorrect arguments given")
        return None

    try:
        # Loop for length of objects list
        for i in range(len(objects) - 1):

            # Get top center of current and bottom center of next objects
            current_top = get_center_point(objects[i], top=True)
            next_bottom = get_center_point(objects[i+1], bottom=True)

            # Move the next object so it is resting on the current object
            create_stack(objects[i+1], next_bottom, current_top)

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


def verify_args(objects):
    """
    This function verifies the names of objects in the list and returns the result

    :param objects: A list containing all the objects to be stacked.
    :type: list of strings

    :return: Whether or not any/all of the arguments have a value.
    :type: bool
    """

    objs_clear = True

    for obj in objects:
        if not cmds.objExists(obj):
            print("Object " + obj + " does not have a value")
            objs_clear = False

    # If all of the arguments have a value return True
    if objs_clear:
        return True
    # If one or more arguments don't have a value return None
    else:
        return None

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
