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

from .skip_2 import skip as skip_cls
from .coarsen_2 import coarsen as coarsen_cls
from .free_stream_particles import free_stream_particles as free_stream_particles_cls
from .wall_film_particles import wall_film_particles as wall_film_particles_cls
from .track_pdf_particles import track_pdf_particles as track_pdf_particles_cls

class attributes(Group):
    fluent_name = ...
    child_names = ...
    skip: skip_cls = ...
    coarsen: coarsen_cls = ...
    free_stream_particles: free_stream_particles_cls = ...
    wall_film_particles: wall_film_particles_cls = ...
    track_pdf_particles: track_pdf_particles_cls = ...
