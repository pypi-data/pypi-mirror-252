from operator import (
    call
)
from pythonix.suffix_types import DelayedSuffix
from pythonix.result.decorators import safe

call_obj = DelayedSuffix(safe(call, TypeError)) # type: ignore
get_attr = DelayedSuffix(safe(getattr, AttributeError))
set_attr = DelayedSuffix(safe(setattr, AttributeError))
del_attr = DelayedSuffix(safe(delattr, AttributeError))
has_attr = DelayedSuffix(hasattr)
