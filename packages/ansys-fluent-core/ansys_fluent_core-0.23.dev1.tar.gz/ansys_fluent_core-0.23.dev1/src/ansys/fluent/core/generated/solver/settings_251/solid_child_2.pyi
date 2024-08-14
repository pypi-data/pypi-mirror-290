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

from typing import Union, List, Tuple

from .name_1 import name as name_cls
from .type_4 import type as type_cls
from .location_2 import location as location_cls
from .settings_29 import settings as settings_cls
from .boundaries import boundaries as boundaries_cls
from .split import split as split_cls

class solid_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    type: type_cls = ...
    location: location_cls = ...
    settings: settings_cls = ...
    boundaries: boundaries_cls = ...
    command_names = ...

    def split(self, name: str, location: List[str]):
        """
        Input volume name to split.
        
        Parameters
        ----------
            name : str
                Input new volume name.
            location : typing.List[str]
                Input location name which should be part of new volume.
        
        """

