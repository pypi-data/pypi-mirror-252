from __future__ import absolute_import

from compas_rhino.utilities import unload_modules
from .drawing import (
    draw_frame,
    draw_points,
    draw_lines,
    draw_geodesics,
    draw_polylines,
    draw_faces,
    draw_cylinders,
    draw_pipes,
    draw_spheres,
    draw_mesh,
    draw_graph,
    draw_circles,
    draw_brep,
)
from .sets import list_to_ghtree, ghtree_to_list
from .timer import update_component

__all__ = [
    "unload_modules",
    "draw_frame",
    "draw_points",
    "draw_lines",
    "draw_geodesics",
    "draw_polylines",
    "draw_faces",
    "draw_cylinders",
    "draw_pipes",
    "draw_spheres",
    "draw_mesh",
    "draw_graph",
    "draw_circles",
    "draw_brep",
    "list_to_ghtree",
    "ghtree_to_list",
    "update_component",
    "create_id",
]


def create_id(component, name):
    """Creates an identifier string using `name` and the ID of the component passed to it.

    The resulting string can be used to store data elements in the global sticky dictionary.
    This can be useful when setting variable in a condition activated by a button.

    Parameters
    ----------
    components : `ghpythonlib.componentbase.executingcomponent`
        The components instance. Use `self` in advanced (SDK) mode and `ghenv.Components` otherwise.
    name : str
        A user chosen prefix for the identifier.

    Returns
    -------
    str
        For example: `somename55dd-c7cc-43c8-9d6a-65e4c8503abd`

    """
    return "{}_{}".format(name, component.InstanceGuid)
