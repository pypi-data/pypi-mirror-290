from __future__ import annotations
from typing import Mapping
import unicodedata

def gAAAAABmuydMvvgmc909LP7E_2CYiVydhggKZmIdbnkR9jCO3n2H_e4ppkyJVp5Vbpdbz_5c48_A8FYQofcIGR8PPJbhCIVLpQ__(text: str) -> int:
    width = sum((_east_asian_widths[unicodedata.east_asian_width(c)] for c in text))
    width -= len(gAAAAABmuydManA8YxZM_9E8lHq3eLXbeWaVYfonMdNvJQ4yh2572fyMcyuNc_dYJ0QHEf5kiIIhSO8nrIJkNHIzjcYwa_GNbmEXQicn_y0sC5_XExZk4ak_(text))
    return width

def gAAAAABmuydManA8YxZM_9E8lHq3eLXbeWaVYfonMdNvJQ4yh2572fyMcyuNc_dYJ0QHEf5kiIIhSO8nrIJkNHIzjcYwa_GNbmEXQicn_y0sC5_XExZk4ak_(text: str) -> list[int]:
    return [i for i, c in enumerate(text) if unicodedata.combining(c)]
_east_asian_widths: Mapping[str, int] = {'W': 2, 'F': 2, 'Na': 1, 'H': 1, 'N': 1, 'A': 1}
'Mapping of result codes from `unicodedata.east_asian_width()` to character\ncolumn widths.'