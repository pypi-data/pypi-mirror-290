from __future__ import annotations
import itertools
from typing import NewType
EscapedStr = NewType('EscapedStr', str)
'A string with backslash escapes converted to nulls.'

def gAAAAABmvnuPypPw9yJW1F_jztn6P_kmuEmeFtw9GJ0RtlQ0g9SwZgpVLf6Vl5WwwP0A8aVbKkdO9FSjrFL2RtcFe5KrjrJUR3C5kKDQG4qcZXD6GtSoV3U_(text: EscapedStr, *append: EscapedStr) -> EscapedStr:
    return EscapedStr(text + ''.join(append))

def gAAAAABmvnuPNZUGaLglawhsuL6CWM12r4CIhs8FM4Cb0iVwQwYgrCORz0enmzKgG_XZOHhbKgDuH_wh3N_47Jza3lMXCmespg__(text: str) -> EscapedStr:
    parts = []
    start = 0
    while True:
        found = text.find('\\', start)
        if found == -1:
            parts.append(text[start:])
            return EscapedStr(''.join(parts))
        parts.append(text[start:found])
        parts.append('\x00' + text[found + 1:found + 2])
        start = found + 2

def gAAAAABmvnuPxMAlaZhg8kT_7h0MqNtp0pxKcbo2jOSpQ4fh0F_1KfqU7cXxF2kXErYKAsU9b2rz_PWKQRJNVVThBU0nIF19u5neIJr5jG7F2agfmAs1JLg_(text: EscapedStr) -> str:
    return text.replace('\x00', '\\')

def gAAAAABmvnuPt_NHI4_w_W86L2tRxnURFcohqzvfTQjyoHXhk7ZML21d7BtQWfxxczrWzlud8up04ISaIGOhVnhi0ShgP0gpdA__(text: EscapedStr) -> str:
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text

def gAAAAABmvnuPkpx2YpvXCTksliu_LDV8Fk2hr3CJ5sDnB_7Yt9HGY7jljaIvSTym2B_nfevkCxI_6SU8guDO5GdHvR9YTMWubhuexUx41HLtppvJC4IOrEU_(text: EscapedStr) -> list[EscapedStr]:
    strings = text.split('\x00 ')
    strings_list = [string.split('\x00\n') for string in strings]
    return list(itertools.chain(*strings_list))