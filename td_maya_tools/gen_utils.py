#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    username

:synopsis:
    A one line summary of what this module does.

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
    def _getitem_(self,item):
        try:
            return dict._getitem_(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value








