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

from qgis.utils import qgsfunction
from qgis.core import QgsExpression, QgsApplication
from .three_toolbox_provider import ThreeToolboxProvider
from .core.mesh import Mesh

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

@qgsfunction('auto', "3D Geometry", register=False)
def volume(geometry, feature, parent):
    """
        Returns the volume of a geometry multipolygon object. If the geometry is
        not a closed volume, this can be an arbitrary value.

        <h4>Syntax</h4>
        <div class="syntax">
            <code>
                <span class="functionname">volume</span>
                (<span class="argument">geometry</span>)
            </code>
            <br/><br/>[ ] marks optional components
        </div>

        <h4>Arguments</h4>
        <div class="arguments">
            <table>
                <tr><td class="argument">geometry</td><td>multipolygon geometry object</td></tr>
            </table>
        </div>

        <h4>Examples</h4>
        <div class="examples">
        <ul>
            <li>
                <code>volume($geometry)</code> &rarr; <code>The volume of the current geometry</code>
            </li>
        </ul>
        </div>
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return 0

    return mesh.volume()

class ThreeToolboxPlugin(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = ThreeToolboxProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()
        QgsExpression.registerFunction(volume)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        QgsExpression.unregisterFunction('volume')
