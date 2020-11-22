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
    A utility file to handle XML files and XML data

:description:
    This module is a utility class for the other parts of the stacker code. It has two
    features. The first is a function which puts the contents of an XML file into a dict
    and the second is a class which is a Python implementation of the autovivification
    feature in Perl.

:applications:

:see_also:
    stacker.py
    builder_gui.py
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
from xml.dom import minidom
import xml.etree.ElementTree as et
import os

# Imports That You Wrote


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def read_stack_xml(xml_path):
    """
    Places the XML contents into a dictionary

    :param xml_path: the path to an XML file on disk
    :type: str

    :return: XML Contents
    :type: dict
    """
    xml_fh = et.parse(xml_path)
    root = xml_fh.getroot()

    #children
    contents = {}
    root_children = root.getchildren()
    for xml_item in root_children:
        contents[xml_item.tag] = ""
    return contents


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
