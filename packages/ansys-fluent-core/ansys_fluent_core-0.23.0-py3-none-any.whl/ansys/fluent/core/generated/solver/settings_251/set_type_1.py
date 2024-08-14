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

from .volumes_names import volumes_names as volumes_names_cls
from .type_5 import type as type_cls

class set_type(Command):
    """
    Input volume name(s) to change its type.
    
    Parameters
    ----------
        volumes_names : List
            Input volume names .
        type : str
            Input volume type.
    
    """

    fluent_name = "set-type"

    argument_names = \
        ['volumes_names', 'type']

    _child_classes = dict(
        volumes_names=volumes_names_cls,
        type=type_cls,
    )

