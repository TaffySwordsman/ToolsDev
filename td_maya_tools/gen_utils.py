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
 #Make sure file exists
    if not os.path.isfile(xml_path):
        print'The file does not exist'
        return None

    #Read in the XML and get the root
    xml_fh = et.parse(xml_path)
    root = xml_fh.getroot()

    #children
    contents = Autovivification()
    xml_num = root.getchildren()
    for xml_numb in xml_num:
        xml_tran =xml_numb.getchildren()
        for xml_mov in xml_tran:
            value = xml_mov.attrib['value']
            contents[xml_numb.tag] [xml_mov.tag] = value
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
