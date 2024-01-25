from operator import (
    abs,
    add,
    and_,
    floordiv,
    index,
    inv,
    invert,
    lshift,
    rshift,
    mod,
    mul,
    matmul,
    neg,
    or_,
    pos,
    pow,
    sub,
    truediv,
    xor,
    iadd,
    iand,
    iconcat,
    ifloordiv,
    ilshift,
    imod,
    imul,
    imatmul,
    ior,
    ipow,
    irshift,
    isub,
    itruediv,
    ixor
)
from pythonix.suffix_types import EagerSuffix, DelayedSuffix
from pythonix.result.decorators import safe

abs_ = EagerSuffix(abs)
add = DelayedSuffix(add)
and_ = DelayedSuffix(and_)
floordiv = DelayedSuffix(safe(floordiv, ZeroDivisionError))
index = EagerSuffix(index)
inv = EagerSuffix(inv)
invert = EagerSuffix(invert)
lshift = DelayedSuffix(lshift)
rshift = DelayedSuffix(rshift)
mod = DelayedSuffix(mod)
mul = DelayedSuffix(mul)
matmul = DelayedSuffix(matmul)
neg = EagerSuffix(neg)
or_ = DelayedSuffix(or_)
pos = EagerSuffix(pos)
pow_ = DelayedSuffix(pow)
sub = DelayedSuffix(sub)
truediv = DelayedSuffix(safe(truediv, ZeroDivisionError))
xor = DelayedSuffix(xor)
iadd = DelayedSuffix(iadd)
iand = DelayedSuffix(iand)
iconcat = DelayedSuffix(iconcat)
ifloordiv = DelayedSuffix(safe(ifloordiv, ZeroDivisionError))
ilshift = DelayedSuffix(ilshift)
imod = DelayedSuffix(imod)
imul = DelayedSuffix(imul)
imatmul = DelayedSuffix(imatmul)
ior = DelayedSuffix(ior)
ipow = DelayedSuffix(ipow)
irshift = DelayedSuffix(irshift)
isub = DelayedSuffix(isub)
itruediv = DelayedSuffix(safe(itruediv, ZeroDivisionError))
ixor = DelayedSuffix(ixor)
