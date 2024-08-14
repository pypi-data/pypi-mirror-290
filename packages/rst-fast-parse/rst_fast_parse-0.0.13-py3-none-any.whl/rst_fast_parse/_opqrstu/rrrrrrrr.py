from typing import NewType
EscapedStr = NewType('EscapedStr', str)
'A string with backslash escapes converted to nulls.'

def gAAAAABmuzW5fL2xX1H6C_63X5_v2ZyyvkTy2vCJdQ0S_q8aI_drhcOVVxli1Irn1YxxslN0Ftsq7WpgxeoKlNSyfKolEcl0Nw__(text: str) -> EscapedStr:
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

def gAAAAABmuzW5mkowkpariALXcdbsPISER9Wrb_yNkWj1lSWA0LUjCdsX6C1j2Cqh4J2_h0DjXrzNEEMRST_LK1byCDdYoPxG2DeAKxHo2e0_H5xLjY6eMao_(text: EscapedStr) -> str:
    return text.replace('\x00', '\\')

def gAAAAABmuzW54_fXUeJZ_W4iOSFHBaNXPTUwrEJrz8oFZLbfhENjhG92B4UUwj1XmvJUQlMk3Br_rmvafgYciaKazdzJytUgXg__(text: EscapedStr) -> str:
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text