import thirdai._thirdai.bolt
from thirdai._thirdai.bolt import *

from .udt_modifications import (
    add_neural_index_aliases,
    modify_graph_udt,
    modify_mach_udt,
    modify_udt,
)

modify_udt()
modify_graph_udt()
modify_mach_udt()
add_neural_index_aliases()

try:
    # This is to prevent errors if torch or scipy are not installed.
    # They are used in the seismic model but not the main thirdai package.
    from .seismic_modifications import modify_seismic

    modify_seismic()
except ImportError:
    pass

__all__ = []
__all__.extend(dir(thirdai._thirdai.bolt))
