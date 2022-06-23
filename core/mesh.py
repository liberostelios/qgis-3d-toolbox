"""A module that defines the Mesh class"""

from typing import Tuple
from xmlrpc.client import Boolean
import pyvista as pv
import numpy as np
from qgis.core import QgsGeometry, QgsMultiLineString, QgsLineString, QgsPolygon
import triangle as tr

def polydata_to_geom(polydata) -> QgsGeometry:
    """Returns a QgsGeometry from a pyvista mesh"""
    lines = QgsMultiLineString()

    for i in range(polydata.n_cells):
        lines.addGeometry(QgsLineString(polydata.cell_points(i)))

    return lines

def vector_angle(va, vb):
    """Returns the angle between two vectors (in degrees)"""
    a = np.array(va)
    b = np.array(vb)

    inner = np.inner(a, b)
    norms = np.linalg.norm(a) * np.linalg.norm(b)

    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    deg = np.rad2deg(rad)

    return deg.item()

def newells_normals(poly):
    """Returns the normal of a surface."""
    n = [0.0, 0.0, 0.0]

    for i, v_curr in enumerate(poly):
        v_next = poly[(i+1) % len(poly)]
        n[0] += (v_curr[1] - v_next[1]) * (v_curr[2] + v_next[2])
        n[1] += (v_curr[2] - v_next[2]) * (v_curr[0] + v_next[0])
        n[2] += (v_curr[0] - v_next[0]) * (v_curr[1] + v_next[1])

    if all([c == 0 for c in n]):
        raise ValueError("No normal. Possible colinear points!")

    normalised = [i/np.linalg.norm(n) for i in n]

    return normalised

def axes_of_normal(normal):
    """Returns an x-axis and y-axis on a plane of the given `normal`"""
    if normal[2] > 0.001 or normal[2] < -0.001:
        x_axis = [1, 0, -normal[0]/normal[2]]
    elif normal[1] > 0.001 or normal[1] < -0.001:
        x_axis = [1, -normal[0]/normal[1], 0]
    else:
        x_axis = [-normal[1] / normal[0], 1, 0]

    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(normal, x_axis)

    return x_axis, y_axis

def project_2d(points, normal, origin=None) -> list:
    """
    Projects the 3d `points` provided to a local coordinates on the 2d plane
    defined by `normal`.
    """
    if origin is None:
        origin = points[0]

    x_axis, y_axis = axes_of_normal(normal)

    return [[np.dot(p - origin, x_axis), np.dot(p - origin, y_axis)] for p in points]

def triangulate_polygon(points, offset = 0):
    """Returns the points and triangles for a given CityJSON polygon"""

    normal = surface_normal(points)
    holes = [0]
    for ring in face:
        holes.append(len(ring) + holes[-1])
    holes = holes[1:]

    points_2d = project_2d(points, normal)

    result = earcut.triangulate_float32(points_2d, holes)

    result += offset

    t_count = len(result.reshape(-1,3))
    if t_count == 0:
        return points,  []
    triangles = np.hstack([[3] + list(t) for t in result.reshape(-1,3)])

    return points, triangles

class Polygon:
    """
    A class that represents a polygon.

    This is used to compute the triangulation while converting from QgsGeometry
    to PolyData.
    """

    def __init__(self, polygon: QgsPolygon):
        self.__outerRing = self.curveToRing(polygon.exteriorRing())

        self.__innerRings = []
        for i in range(polygon.numInteriorRings()):
            self.__innerRings.append(self.curveToRing(polygon.interiorRing(i)))

    def curveToRing(self, curve):
        """Converts a QgsCurve to a list of points"""
        pts = curve.points()

        return [[p.x(), p.y(), p.z()] for p in pts]

    @property
    def normal(self):
        """Returns the polygon's normal vector"""
        return newells_normals(self.__outerRing)

    def triangulate(self, offset=0) -> Tuple[list, list]:
        """Returns the points and triangles that represent a triangulation of
        the polygon."""
        normal = self.normal

        points = self.__outerRing.copy()

        # Compute the offsets of the holes
        # holes = [0]
        # for ring in self.__innerRings:
        #     points.extend(ring)
        #     holes.append(len(ring) + holes[-1])
        # holes = holes[1:] + [len(points)]

        points = np.array(points)

        points_2d = project_2d(points, normal)[:-1]

        segments = [[i, i+1] for i in range(len(points_2d) - 1)] + [[len(points_2d) - 1, 0]]

        # result = earcut.triangulate_float32(points_2d, holes)

        # result += offset

        # t_count = len(result.reshape(-1,3))
        # if t_count == 0:
        #     return points,  []
        # triangles = np.hstack([[3] + list(t) for t in result.reshape(-1,3)])

        data = {
            'vertices': points_2d,
            'segments': segments
        }
        T = tr.triangulate(data, 'p')
        result = T["triangles"] + offset

        triangles = np.hstack([[3] + list(t) for t in result])

        return points, triangles

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
        self.__polydata = mesh

        if not self.isEmpty():
            self.clean(tolerance)

    def clean(self, tolerance):
        """Removes duplicate vertices and cleans the dataset"""
        self.__polydata = self.__polydata.clean(tolerance=tolerance)

    def geom_to_polydata(self, geometry: QgsGeometry, triangulate: Boolean = True) -> pv.PolyData:
        """Converts a QgsGeometry to PolyData"""
        points = []
        faces = []

        for part in geometry.parts():
            try:
                poly = Polygon(part)
                p, t = poly.triangulate(len(points))
            except Exception:
                continue
            
            points.extend(p)
            faces.extend(t)

        if len(points) == 0:
            return pv.PolyData()

        mesh = pv.PolyData(points, faces)

        # mesh.plot()

        return mesh

    def triangulate(self) -> None:
        """Triangulates the mesh"""


    def polydata(self) -> pv.PolyData:
        """Returns the polydata object"""
        return self.__polydata

    def area(self) -> float:
        """Returns the surface area of the mesh"""
        return float(self.__polydata.area)

    def volume(self) -> float:
        """Returns the volume of the given geometry"""
        return float(self.__polydata.volume)

    def slopes(self) -> list:
        """Returns the slope of individual surface of the geometry"""
        zenith = [0, 0, 1]
        normals = self.__polydata.cell_normals

        return [vector_angle(n.tolist(), zenith) for n in normals]

    def isEmpty(self) -> bool:
        """Returns True if the geometry is empty"""
        return self.__polydata.n_points == 0 or self.__polydata.n_cells == 0

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
