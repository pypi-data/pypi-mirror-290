from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
'The largest number representable as a roman numeral.'

def gAAAAABmuydM_lEjOuv0igMhKwaEDmZkZeXWn3FNcHII6TaN5GrxOwghlD9t_kTwB6R11IV9mdz_0y5Py6g_Ejr_bQ0_AdDABg__(n: int) -> None | str:
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

def gAAAAABmuydMY3I_RXHry2ThhmPLXAUfjoPO8FQAVsM3W7uaX1XSwqqj7fpURuBzIye3sd7HHpbsoobDgBVE1QoAnq7VAmNxKw__(txt: str) -> None | int:
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

def gAAAAABmuydMDKn8AiAPEus6utiXPVbHyEXVdp2Zjo3NLRdr7KzDnbxXYhywOUCC29nvxg4YbR6rGSn_4QH4K6UvcsHPfFSt_w__(txt: str) -> None | int:
    if txt == 'N':
        return 0
    if (n := gAAAAABmuydMY3I_RXHry2ThhmPLXAUfjoPO8FQAVsM3W7uaX1XSwqqj7fpURuBzIye3sd7HHpbsoobDgBVE1QoAnq7VAmNxKw__(txt)) is None:
        return None
    if gAAAAABmuydM_lEjOuv0igMhKwaEDmZkZeXWn3FNcHII6TaN5GrxOwghlD9t_kTwB6R11IV9mdz_0y5Py6g_Ejr_bQ0_AdDABg__(n) == txt:
        return n
    return None