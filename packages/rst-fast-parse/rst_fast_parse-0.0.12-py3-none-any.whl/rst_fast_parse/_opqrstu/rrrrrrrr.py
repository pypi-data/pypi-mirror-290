from typing import NewType
EscapedStr = NewType('EscapedStr', str)
'A string with backslash escapes converted to nulls.'

def gAAAAABmuydMPtls5CUMo4erY_jQ1TheJVFpl8HAqeRri9_rhhWIJrda9Yub4Uvd5f_gKwEQ6IEM95TCD8LOzlPvMlhxft3lIw__(text: str) -> EscapedStr:
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

def gAAAAABmuydML19K8X75ay8cEWNwmjBmjTUqw9mjKLZRoIzpHQod13eo0PQ7nIDleSKX_JHkvc78D40g8_rHkp6IFIkUD_AI71eTKto2uhZj2YZUkxWx60E_(text: EscapedStr) -> str:
    return text.replace('\x00', '\\')

def gAAAAABmuydMiEstuu8RD1fjnJiyhjBfoPmwpwnvYhRdcpXnN0E9zwayiK__30RnJtz2MObxTiDpfu_i0v2CEjG_ENTVBnHqoA__(text: EscapedStr) -> str:
    if '\x00' not in text:
        return text
    for sep in ['\x00 ', '\x00\n', '\x00']:
        text = ''.join(text.split(sep))
    return text