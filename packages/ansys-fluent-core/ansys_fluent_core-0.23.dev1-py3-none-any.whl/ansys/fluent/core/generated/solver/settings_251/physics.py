#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .fluid_2 import fluid as fluid_cls
from .solid_3 import solid as solid_cls
from .interfaces import interfaces as interfaces_cls
from .list_physics import list_physics as list_physics_cls

class physics(Group, _ChildNamedObjectAccessorMixin):
    """
    'physics' child.
    """

    fluent_name = "physics"

    child_names = \
        ['fluid', 'solid', 'interfaces']

    command_names = \
        ['list_physics']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
        interfaces=interfaces_cls,
        list_physics=list_physics_cls,
    )

