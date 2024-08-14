from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmuzW596NImKClG_i2pAO8HW6g5MI1RBVdg1u0mNqZS2XTzZfa4uQRkADvsoKIhc5_P_E1RmjftjA75XHCHX56K3F8sA__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmuzW5WRDKFy93I0Bo3X_Fv3A_WqB13H3fROUFy0GnlqR94eF5nAiYFZ_K_Kjyyut3jwc9ODbW9j10boCEHwxB2Uhw2_w5X4RfFN6PjQKBv1owlNY_(text))
    return width

def gAAAAABmuzW5WRDKFy93I0Bo3X_Fv3A_WqB13H3fROUFy0GnlqR94eF5nAiYFZ_K_Kjyyut3jwc9ODbW9j10boCEHwxB2Uhw2_w5X4RfFN6PjQKBv1owlNY_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'