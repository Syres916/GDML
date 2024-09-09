# -*- coding: utf-8 -*-
# Fri Feb 11 01:11:14 PM PST 2022
# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2024 Keith Sloan <keith@sloan-home.co.uk>              *
# *                                                                        *
# *   This program is free software; you can redistribute it and/or modify *
# *   it under the terms of the GNU Lesser General Public License (LGPL)   *
# *   as published by the Free Software Foundation; either version 2 of    *
# *   the License, or (at your option) any later version.                  *
# *   for detail see the LICENCE text file.                                *
# *                                                                        *
# *   This program is distributed in the hope that it will be useful,      *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# *   GNU Library General Public License for more details.                 *
# *                                                                        *
# *   You should have received a copy of the GNU Library General Public    *
# *   License along with this program; if not, write to the Free Software  *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# *   USA                                                                  *
# *                                                                        *
# *   Acknowledgements :
# *                                                                        *
# *                                                                        *
# **************************************************************************
__title__ = "FreeCAD - Fluka Importer using pyg4omtery"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

import FreeCAD, FreeCADGui
import os, io, sys, re

from PySide import QtGui, QtCore

def joinDir(path):
    import os
    __dirname__ = os.path.dirname(__file__)
    return(os.path.join(__dirname__, path))

# Save the native open function to avoid collisions
if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open  # to distinguish python built-in open function from the one declared her


def open(filename):
    "called when freecad opens a file."

    print('Open : '+filename)
    docName = os.path.splitext(os.path.basename(filename))[0]
    print('path : '+filename)
    if filename.lower().endswith('.inp'):
        try:
            doc = FreeCAD.ActiveDocument()
            print('Active Doc')

        except:
            print('New Doc')
            doc = FreeCAD.newDocument(docName)

        processFluka(doc, filename)
        return doc


def insert(filename, docname):
    "called when freecad imports a file"
    print('Insert filename : '+filename+' docname : '+docname)
    global doc
    groupname = os.path.splitext(os.path.basename(filename))[0]
    try:
        doc = FreeCAD.getDocument(docname)
    except NameError:
        doc = FreeCAD.newDocument(docname)
    if filename.lower().endswith('.inp'):
        processFluka(doc, filename)


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))



def processFluka(doc, filePath):

    import pyg4ometry.fluka as fluka
    import pyg4ometry.gdml as gdml
    from pyg4ometry.convert import fluka2Geant4

    # Read the FLUKA file, get the FlukaRegistry, convert the registry to a
    # Geant4 Registry
    import FreeCADGui 
    from . import GDMLUtils
    from .importGDML  import processGDML

    from datetime import datetime
    print("Check Materials definitions exist")
    #checkMaterialDefinitionsExist()
    startTime = datetime.now()
    tempFile = GDMLUtils.getTempFileName(filePath,".gdml")
    #print(f"Temp gdml file {tempFileGen}")

    #reader = fluka.Reader("model.inp")
    reader = fluka.Reader(filePath)
    flukaRegistry = reader.flukaregistry
    geant4Registry = fluka2Geant4(flukaRegistry)
    worldLogicalVolume = geant4Registry.getWorldVolume()
    worldLogicalVolume.clipSolid()

    writer = gdml.Writer()
    writer.addDetector(geant4Registry)
    # writer.write("model.gdml")
    #writer.write("/tmp/tempGDML.gdml")
    writer.write(tempFile)
    FreeCADGui.setActiveDocument(doc)
    processGDML(doc, False, tempFile, False, 1, 0)
    # doc, open=False, filename, prompt Process, processType 1 = GDML
    FreeCAD.ActiveDocument.recompute()
    if FreeCAD.GuiUp:
        FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCAD.Console.PrintMessage("End import Fluka inp file\n")
