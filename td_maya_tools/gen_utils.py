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
    A detailed description of what this module does.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.
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
    def _getitem_(self,item):
        """
        Might need to be a function not a class

        :param item:
        :type:

        :return: XML value of item
        :type:
        """
        try:
            return dict._getitem_(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value








