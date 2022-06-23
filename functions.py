from qgis.utils import qgsfunction
from .core.mesh import Mesh

functions_help = {
    "volume": """
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
    """,
    "is_solid": """
        Returns true if a given multipolygon object is a closed volume.

        <h4>Syntax</h4>
        <div class="syntax">
            <code>
                <span class="functionname">is_solid</span>
                (<span class="argument">geometry</span>)
            </code>
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
                <code>is_solid($geometry)</code> &rarr; <code>true (if, the current geometry is closed)</code>
            </li>
        </ul>
        </div>
    """,
    "surface_area": """
        Returns the surface area of a multipolygon geometry.

        <h4>Syntax</h4>
        <div class="syntax">
            <code>
                <span class="functionname">surface_area</span>
                (<span class="argument">geometry</span>)
            </code>
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
                <code>surface_area($geometry)</code> &rarr; <code>The surface area of the current geometry</code>
            </li>
        </ul>
        </div>
    """,
    "slope": """
        Returns the slope of a polygon geometry.

        <h4>Syntax</h4>
        <div class="syntax">
            <code>
                <span class="functionname">slope</span>
                (<span class="argument">geometry</span>)
            </code>
        </div>

        <h4>Arguments</h4>
        <div class="arguments">
            <table>
                <tr><td class="argument">geometry</td><td>polygon geometry object</td></tr>
            </table>
        </div>

        <h4>Examples</h4>
        <div class="examples">
        <ul>
            <li>
                <code>slope($geometry)</code> &rarr; <code>The slope of the current geometry</code>
            </li>
        </ul>
        </div>
    """
}

@qgsfunction('auto', "3D Geometry", register=False, helpText=functions_help["volume"])
def volume(geometry, feature, parent):
    """Returns the volume of a multipolygon geometry. If the geometry is
    not a closed volume, this can be an arbitrary value.

    Parameters
    ----------
    geometry : QgsGeometry
        A multipolygon geometry
    feature : QgsFeature
        The current feature (unused)
    parent : any
        The parent feature (unused)

    Returns
    -------
    float
        The volume bounded by the current geometry
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return 0

    return mesh.volume()

@qgsfunction('auto', "3D Geometry", register=False, helpText=functions_help["is_solid"])
def is_solid(geometry, feature, parent):
    """Returns `True` if a given multipolygon object is a closed volume.

    Parameters
    ----------
    geometry : QgsGeometry
        A multipolygon geometry
    feature : QgsFeature
        The current feature (unused)
    parent : any
        The parent feature (unused)

    Returns
    -------
    bool
        Return `True` if there are no holes on the geometry.
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return False

    return mesh.isSolid()

@qgsfunction('auto', "3D Geometry", register=False, helpText=functions_help["surface_area"])
def surface_area(geometry, feature, parent) -> float:
    """Returns the surface area of a multipolygon geometry.

    Parameters
    ----------
    geometry : QgsGeometry
        A multipolygon geometry
    feature : QgsFeature
        The current feature (unused)
    parent : any
        The parent feature (unused)

    Returns
    -------
    float
        The surface area of the geometry
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return 0

    return mesh.area()

@qgsfunction('auto', "3D Geometry", register=False, helpText=functions_help["slope"])
def slope(geometry, feature, parent) -> float:
    """Returns the surface area of a multipolygon geometry.

    Parameters
    ----------
    geometry : QgsGeometry
        A multipolygon geometry
    feature : QgsFeature
        The current feature (unused)
    parent : any
        The parent feature (unused)

    Returns
    -------
    float
        The slope a given surface
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return None

    return mesh.slopes()[0]

@qgsfunction('auto', "3D Geometry", register=False, helpText="Plot for debug reasons")
def plot(geometry, feature, parent) -> float:
    """Returns the surface area of a multipolygon geometry.

    Parameters
    ----------
    geometry : QgsGeometry
        A multipolygon geometry
    feature : QgsFeature
        The current feature (unused)
    parent : any
        The parent feature (unused)

    Returns
    -------
    float
        The surface area of the geometry
    """

    mesh = Mesh(geometry)

    if mesh.isEmpty():
        return None

    mesh.polydata().plot(show_edges=True)

    return 0
