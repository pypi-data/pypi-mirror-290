from typing import NewType
EscapedStr = NewType('EscapedStr', str)
'A string with backslash escapes converted to nulls.'

def gAAAAABmuqBgrHH9Mv_plVN1LzgVJw5afJ5Z_2Dnqo3IOEmV_M0NPg3QbGMY1ePWKWYvMw5pa0QGhqu0MVmzuu52Gf5TjvxYPQ__(text: str) -> EscapedStr:
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

def gAAAAABmuqBg_qFyzGDnI9HEQ_qKjxQNPUZmGupVbsU52cDLFCXzHaNlRtNoupwLQjb6RuA1nHWXRw2tmqzEPsI9herOb2Iq_f6vcVuBi428NNgbEoCsntk_(text: EscapedStr) -> str:
    return text.replace('\x00', '\\')

def gAAAAABmuqBg5F4hPCxSPv5rQRWUXR8VlNwp1E1NRUYadqI4glcsrNl3_SayrLOeO905Db6NVrJPtPGnVew4KWTkYB_rVB1Nsw__(text: EscapedStr) -> str:
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text