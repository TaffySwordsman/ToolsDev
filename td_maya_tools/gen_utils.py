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
    #Make sure file exists
    if not os.path.isfile(xml_path):
        print'The file does not exist'
        return None

    #Read in the XML and get the root
    xml_fh = et.parse(xml_path)
    root = xml_fh.getroot()

    #children
    contents = Autovivification()
    main_xml = root.getchildren()
    for maya_stacks_xml in main_xml:
        stacks_xml_list = maya_stacks_xml.getchildren()
        for stack_xml in stacks_xml_list:
            stack_value = stack_xml.tag
            for obj_xml in stack_xml:
                obj_value = obj_xml.tag
                trans_value = obj_xml.attrib['value']
                contents[stack_value][obj_value] = trans_value
    return contents

    # <?xml version="1.0" ?>
    # <stacks>
    #     <maya_stacks>
    #         <stack001>
    #             <tx value="2"/>
    #             <ty value="0"/>
    #             <tz value="3"/>
    #         </stack001>
    #         <stack002>
    #             <tx value="4.5"/>
    #             <ty value="0"/>
    #             <tz value="4.5"/>
    #         </stack002>
    #         <stack003>
    #             <tx value="5.5"/>
    #             <ty value="1"/>
    #             <tz value="5.5"/>
    #         </stack003>
    #     </maya_stacks>
    # </stacks>


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
