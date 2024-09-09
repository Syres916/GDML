# Mon Aug 26 2024
# Sat Mar 28 8:44 AM PDT 2023
# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2024 Keith Sloan <keith@sloan-home.co.uk>              *
# *             (c) 2024 Munther Hindi
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
# *   Acknowledgements : Ideas & code copied from                          *
# *                      https://github.com/ignamv/geanTipi                *
# *                                                                        *
# ***************************************************************************
__title__ = "FreeCAD - Fluka & Flair exporter enabled by pyg4ometry"
__author__ = "Keith Sloan <keith@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_Geant4"]

import FreeCAD, os
import FreeCADGui
# ***************************************************************************
# Tailor following to your requirements ( Should all be strings )          *
# no doubt there will be a problem when they do implement Value
if open.__module__ in ["__builtin__", "io"]:
    pythonopen = open  # to distinguish python built-in open function from the one declared here

# ## modifs lambda

#################################
# Switch functions
################################


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


def checkDirectory(path):
    if not os.path.exists(path):
        print("Creating Directory : " + path)
        os.mkdir(path)


def export(exportList, filepath):
    "called when FreeCAD exports a file"
    import os, pyg4ometry
    #def exportGDML(first, filepath, fileExt):
    from .exportGDML import export as exportListPath


    path, fileExt = os.path.splitext(filepath)
    print("filepath : " + path)
    print("file extension : " + fileExt)

    extLower = fileExt.lower()
    if extLower == ".inp" or extLower == ".flair":
        # import cProfile, pstats
        # profiler = cProfile.Profile()
        # profiler.enable()
        gdmlFilePath = path + ".gdml"
        print(f"GDML file path {gdmlFilePath}")
        flukaFilePath = path + ".inp"
        exportListPath(exportList, gdmlFilePath)
        print(f"GDML file {gdmlFilePath} written")
        print(f"Fluka file path {flukaFilePath}")
        #reader = pyg4ometry.gdml.Reader("input.gdml")
        reader = pyg4ometry.gdml.Reader(gdmlFilePath)
        reg = reader.getRegistry()
        logical = reg.getWorldVolume()
        freg = pyg4ometry.convert.geant4Reg2FlukaReg(reg)
        w = pyg4ometry.fluka.Writer()
        w.addDetector(freg)
        #w.write("FileName.inp")
        w.write(flukaFilePath)
        print(f"Fluka file {flukaFilePath} written")
        if extLower == ".flair":
            flairFilePath = path + ".flair"
            extent = logical.extent(includeBoundingSolid=True)
            f = pyg4ometry.fluka.Flair(flukaFilePath,extent)
            #f.write("FileName.flair")
            f.write(flairFilePath)
            print(f"Flair file {flairFilePath} written")

        # profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        # stats.print_stats()

