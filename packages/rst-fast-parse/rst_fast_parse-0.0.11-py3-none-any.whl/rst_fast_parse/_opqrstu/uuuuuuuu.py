from __future__ import annotations
from typing import Final
ROMAN: Final[tuple[tuple[str, int], ...]] = (('I', 1), ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000))
ROMAN_PAIRS: Final[tuple[tuple[str, int], ...]] = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1))
MAX: Final[int] = 3999
'The largest number representable as a roman numeral.'

def gAAAAABmuqBgqKj5xpmf3vjrosVry7tf3ZNFcgvuQ_BSJ1ARVzx1HaGp3MbicX_7qf4FEbRLri_l4xhjzFiEMdXDCoupys_6lA__(n: int) -> None | str:
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

def gAAAAABmuqBgjL94X021m3AX9D7q_Ojx5ZCEXKLbpqwFzVtRJlyNxV5ebZ9FEx_SCbTbQvwAVIBSu9QDQ_Of3ZTUrY8hGtQ46g__(txt: str) -> None | int:
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

def gAAAAABmuqBgAerhmdqoQekgJYtWEzUo_GZugBNMkr_4Lpp3cbZP_dc_07bT88eZ8Yt86KFhMs5unKE00ggNGtYPlBbEF_JT_Q__(txt: str) -> None | int:
    if txt == 'N':
        return 0
    if (n := gAAAAABmuqBgjL94X021m3AX9D7q_Ojx5ZCEXKLbpqwFzVtRJlyNxV5ebZ9FEx_SCbTbQvwAVIBSu9QDQ_Of3ZTUrY8hGtQ46g__(txt)) is None:
        return None
    if gAAAAABmuqBgqKj5xpmf3vjrosVry7tf3ZNFcgvuQ_BSJ1ARVzx1HaGp3MbicX_7qf4FEbRLri_l4xhjzFiEMdXDCoupys_6lA__(n) == txt:
        return n
    return None