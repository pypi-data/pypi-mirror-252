from pythonix.suffix_types import EagerSuffix, DelayedSuffix
from pythonix.result.decorators import safe

input_ = EagerSuffix(input)
print_ = DelayedSuffix(print)
open_ = DelayedSuffix(safe(open, IOError))
