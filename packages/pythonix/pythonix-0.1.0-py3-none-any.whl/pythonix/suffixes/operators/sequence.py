from operator import (
    concat,
    contains,
    delitem,
    countOf,
    getitem,
    indexOf,
    setitem,
    length_hint
)
from pythonix.suffix_types import DelayedSuffix
from pythonix.result.decorators import safe
from typing import TypeVar

T = TypeVar('T')

concat_seq = DelayedSuffix(concat)
del_item = DelayedSuffix(safe(delitem, err_type=LookupError))
get_item = DelayedSuffix(safe(getitem, err_type=LookupError))
index_of = DelayedSuffix(safe(indexOf, ValueError))
set_item = DelayedSuffix(safe(setitem, LookupError))
len_hint = DelayedSuffix(length_hint)
count_of = DelayedSuffix(countOf)