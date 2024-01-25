from operator import (
    not_,
    truth,
    is_,
    is_not
)
from pythonix.suffix_types import EagerSuffix, DelayedSuffix

make_not_ = EagerSuffix(not_)
get_truth = EagerSuffix(truth)
is_a = DelayedSuffix(is_)
is_not_a  = DelayedSuffix(is_not)
is_instance = DelayedSuffix(isinstance)
