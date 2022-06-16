# -*- coding: utf-8 -*-

"""
/***************************************************************************
 3DToolbox
                                 A QGIS plugin
 This plugin provides tools and functions for 3D geometries and volumes
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-08-11
        copyright            : (C) 2021 by 3D geoinformation group
        email                : steliosvitalis@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '3D geoinformation group'
__date__ = '2021-08-11'
__copyright__ = '(C) 2021 by 3D geoinformation group'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from qgis.core import QgsExpression, QgsApplication
from .processing.three_toolbox_provider import ThreeToolboxProvider

try:
    import pyvista
    from .functions import *

    has_pyvista = True
except ImportError:
    has_pyvista = False

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class ThreeToolboxPlugin(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = ThreeToolboxProvider(has_pyvista)
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        if has_pyvista:
            QgsExpression.registerFunction(volume)
            QgsExpression.registerFunction(is_solid)
            QgsExpression.registerFunction(surface_area)
            QgsExpression.registerFunction(slope)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        QgsExpression.unregisterFunction('volume')
        QgsExpression.unregisterFunction('is_solid')
        QgsExpression.unregisterFunction('surface_area')
        QgsExpression.unregisterFunction('slope')
