from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmuqBg2XqZkoeAyUVlvuSFxIHXrVi__rS3jrhh6iZIwq9BXe9Fq9aijl8R3hML4oFyPLwcAo8X_ZpvJix__0aanzjDnw__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmuqBge42TdP81ADHSwU9LpUKTKSvHTeaH2wSoNBmFKsQXIOwTVXJ_ZwZcMm4dml8Jcd2D7pfNCMnO78yPv9fhYaRsiRjFjesQIWYqXgcVdyX8oy8_(text))
    return width

def gAAAAABmuqBge42TdP81ADHSwU9LpUKTKSvHTeaH2wSoNBmFKsQXIOwTVXJ_ZwZcMm4dml8Jcd2D7pfNCMnO78yPv9fhYaRsiRjFjesQIWYqXgcVdyX8oy8_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'