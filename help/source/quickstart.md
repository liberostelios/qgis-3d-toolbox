# Getting Started

3D Toolbox provides support for operating over 3D geometries, such as computing volumes, triangulating 3D polygons etc.

## Installation

The toolbox uses [pyvista](https://docs.pyvista.org/) for doing the processing. Therefore, `pyvista` and its respective dependecies have to be installed in QGIS.

### Windows

1. Open the OSGeo4W shell.
2. Run `py_env`.
3. Run `python -m pip install pyvista`

This guide is based on [[1](https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/)].

### MacOS

Your installation depends on your package.

#### Official All-in-one MacOS package

You can install `pyvista` from inside the toolbox.

#### Kyngchaos builds

This uses the official python installation. Therefore just open any terminal and run: `python -m pip install pyvista`.

### Linux

You probably know what to do... But, basically, just `python -m pip install pyvista`.