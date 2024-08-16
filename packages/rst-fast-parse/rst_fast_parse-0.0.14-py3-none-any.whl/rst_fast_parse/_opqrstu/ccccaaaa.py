from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmvnuPL6GQgOHR4HLqYuQ49VPJkBRXkKuwtWf0CXtbEd5HJKRkYe5BBSfcnSoMjmlzbw0FrSPL6D_hesh5TJ6zUfyboA__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmvnuP_bTfwa8u5gNykNdlyYItz1bBDKLVu2SI4iuKlwd_omPBbzilmBbm8PHUlVjCKlJQFWkoJdtTRtaC8hrJ8xX3hKS8L1m9neH6_hmMhrEXz_Q_(text))
    return width

def gAAAAABmvnuP_bTfwa8u5gNykNdlyYItz1bBDKLVu2SI4iuKlwd_omPBbzilmBbm8PHUlVjCKlJQFWkoJdtTRtaC8hrJ8xX3hKS8L1m9neH6_hmMhrEXz_Q_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'