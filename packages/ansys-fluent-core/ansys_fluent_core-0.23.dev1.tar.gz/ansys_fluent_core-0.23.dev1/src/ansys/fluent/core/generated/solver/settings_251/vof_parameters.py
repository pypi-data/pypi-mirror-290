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

from .vof_formulation import vof_formulation as vof_formulation_cls
from .vof_cutoff import vof_cutoff as vof_cutoff_cls
from .vof_courant_number import vof_courant_number as vof_courant_number_cls

class vof_parameters(Group):
    """
    VOF Parameters.
    """

    fluent_name = "vof-parameters"

    child_names = \
        ['vof_formulation', 'vof_cutoff', 'vof_courant_number']

    _child_classes = dict(
        vof_formulation=vof_formulation_cls,
        vof_cutoff=vof_cutoff_cls,
        vof_courant_number=vof_courant_number_cls,
    )

