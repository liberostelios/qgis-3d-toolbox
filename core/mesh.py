"""A module that defines the Mesh class"""

import pyvista as pv
from qgis.core import QgsGeometry

class Mesh:
    """A class that describes a volumetric object"""

    def __init__(self, geometry: QgsGeometry) -> None:
        self.__polydata = self.geom_to_polydata(geometry)

    def geom_to_polydata(self, geometry: QgsGeometry):
        """Converts a QgsGeometry to PolyData"""
        points = []
        faces = []

        for part in geometry.parts():
            pts = part.exteriorRing().points()

            faces.append(len(pts))
            faces.extend([len(points) + i for i in range(len(pts))])

            points.extend([[p.x(), p.y(), p.z()] for p in pts])

        if len(points) == 0:
            return None

        mesh = pv.PolyData(points, faces)

        return mesh.clean()

    def polydata(self):
        """Returns the polydata object"""
        return self.__polydata

    def volume(self):
        """Returns the volume of the given geometry"""
        return self.__polydata.volume

    def isEmpty(self):
        """Returns True if the geometry is empty"""
        return self.__polydata is None

    def isSolid(self):
        """Returns True if this mesh is a solid (i.e. a closed volume)"""
        return self.__polydata.n_open_edges == 0
