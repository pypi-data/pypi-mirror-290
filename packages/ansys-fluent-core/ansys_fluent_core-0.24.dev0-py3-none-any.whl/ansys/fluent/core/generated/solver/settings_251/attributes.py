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

from .step_size_1 import step_size as step_size_cls
from .tolerance_4 import tolerance as tolerance_cls
from .step import step as step_cls
from .skip_1 import skip as skip_cls
from .coarsen_1 import coarsen as coarsen_cls
from .onzone import onzone as onzone_cls

class attributes(Group):
    """
    'attributes' child.
    """

    fluent_name = "attributes"

    child_names = \
        ['step_size', 'tolerance', 'step', 'skip', 'coarsen', 'onzone']

    _child_classes = dict(
        step_size=step_size_cls,
        tolerance=tolerance_cls,
        step=step_cls,
        skip=skip_cls,
        coarsen=coarsen_cls,
        onzone=onzone_cls,
    )

