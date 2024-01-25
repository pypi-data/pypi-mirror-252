from operator import (
    lt,
    le, 
    eq,
    ne,
    ge,
    gt
)
from pythonix.suffix_types import DelayedSuffix

lt = DelayedSuffix(lt)
le = DelayedSuffix(le)
eq = DelayedSuffix(eq)
ne = DelayedSuffix(ne)
ge = DelayedSuffix(ge)
gt = DelayedSuffix(gt)
