"""A module that defines the Mesh class"""

import pyvista as pv
from qgis.core import QgsGeometry, QgsMultiLineString, QgsLineString

def polydata_to_geom(polydata) -> QgsGeometry:
    """Returns a QgsGeometry from a pyvista mesh"""

    lines = QgsMultiLineString()

    for i in range(polydata.n_cells):
        lines.addGeometry(QgsLineString(polydata.cell_points(i)))

    return lines

class Mesh:
    """A class that describes a volumetric object"""

    def __init__(self, geometry: QgsGeometry, tolerance=None) -> None:
        """Generates the mesh object from a given QgsGeometry.

        Parameters
        ----------
        geometry : QgsGeometry
            The multipolygon geometry
        tolerance : float, optional
            The tolerance used to merge vertices together, by default None. If
            None is used, then only exactly similar vertices will be merged.
        """
        mesh = self.geom_to_polydata(geometry)
        self.__polydata = mesh.clean(tolerance=tolerance)

    def geom_to_polydata(self, geometry: QgsGeometry) -> pv.PolyData:
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

        return mesh

    def polydata(self) -> pv.PolyData:
        """Returns the polydata object"""
        return self.__polydata

    def area(self) -> float:
        """Returns the surface area of the mesh"""
        return float(self.__polydata.area)

    def volume(self) -> float:
        """Returns the volume of the given geometry"""
        return float(self.__polydata.volume)

    def isEmpty(self) -> bool:
        """Returns True if the geometry is empty"""
        return self.__polydata is None

    def isSolid(self) -> bool:
        """Returns True if this mesh is a solid (i.e. a closed volume)"""
        return self.num_of_holes() == 0

    def num_of_holes(self) -> int:
        """Returns the number of open holes in the volume"""
        return self.__polydata.n_open_edges

    def getHoles(self) -> QgsMultiLineString:
        """Returns the open holes of the mesh as QgsMultiLineString"""
        edges = self.__polydata.extract_feature_edges(feature_edges=False,
                                                      manifold_edges=False)

        return polydata_to_geom(edges)
