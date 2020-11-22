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
    This module contains logic for Autovivification and an XML reader

:description:
    This module is a utility class for the other parts of the stacker code. It has two
    features. The first is a function which puts the contents of an XML file into a dict
    and the second is a class which is a Python implementation of the autovivification
    feature in Perl.

:applications:
    Maya

:see_also:
    stacker.py
    builder_gui.py
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


def read_stack_xml(path):
    """
    Puts the contents of an XML file into a dictionary

    :param path: The path to an XML file on disk.
    :type: str

    :return: A dictionary containing the contents of the XML file
    :type: dict
    """

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#


class Autovivification(dict):
    """
    This is a python implementation of Perl's autovivification feature
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
