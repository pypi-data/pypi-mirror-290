from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
'The largest number representable as a roman numeral.'

def gAAAAABmuzW5FeLr8986fw3a0twiNU2ttj9RaCyvfg2YAAw4kwSWa_g_B4lsNtneR3dhBW34rwlUTDeXu3H8c_yCRtfFekwpEA__(n: int) -> None | str:
    if n == 0:
        return 'N'
    if n > MAX:
        return None
    out = ''
    for name, value in ROMAN_PAIRS:
        while n >= value:
            n -= value
            out += name
    assert n == 0
    return out

def gAAAAABmuzW5gn_CzLzCJTqPubV0F2qTC4CpAHqM4AAcUePb_WDD2e4oZeItACaWifkS3YEttzr38c_nXdfe223I1KHJDP0QDw__(txt: str) -> None | int:
    n = 0
    max_val = 0
    for c in reversed(txt):
        it = next((x for x in ROMAN if x[0] == c), None)
        if it is None:
            return None
        _, val = it
        if val < max_val:
            n -= val
        else:
            n += val
            max_val = val
    return n

def gAAAAABmuzW5oBG14suyc2iIFboFLg3wGhmEkSudByNQqDbYUdkLtKmzz2nnEqMqQBJscQJg3soNKMn_HRTKSst3lJ_3_6N8_g__(txt: str) -> None | int:
    if txt == 'N':
        return 0
    if (n := gAAAAABmuzW5gn_CzLzCJTqPubV0F2qTC4CpAHqM4AAcUePb_WDD2e4oZeItACaWifkS3YEttzr38c_nXdfe223I1KHJDP0QDw__(txt)) is None:
        return None
    if gAAAAABmuzW5FeLr8986fw3a0twiNU2ttj9RaCyvfg2YAAw4kwSWa_g_B4lsNtneR3dhBW34rwlUTDeXu3H8c_yCRtfFekwpEA__(n) == txt:
        return n
    return None