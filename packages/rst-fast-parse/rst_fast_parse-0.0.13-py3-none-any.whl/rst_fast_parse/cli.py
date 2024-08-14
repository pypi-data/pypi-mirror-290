from __future__ import annotations
import argparse
from pathlib import Path
import sys
from rst_fast_parse.parse import parse_string

def gAAAAABmuzW5Rgo2fpOYrjmUVblXLwzDIAz3alc76ZYhbJOInvbovRhd6UVCvaqS_MEyUQfdK0d_I1AlO9_v900Vx4nKpLheFQ__() -> None:
    parser = argparse.ArgumentParser(description='Parser CLI')
    parser.add_argument('input', help='Path to the file to parse or - for stdin')
    args = parser.parse_args()
    path: str = args.input
    if path == '-':
        result = parse_string(sys.stdin.read())
    else:
        result = parse_string(Path(path).read_text('utf8'))
    for el in result[0]:
        print(f'{el.tagname:<16} {el.line_range[0] + 1}:{el.line_range[1] + 1}')
if __name__ == '__main__':
    gAAAAABmuzW5Rgo2fpOYrjmUVblXLwzDIAz3alc76ZYhbJOInvbovRhd6UVCvaqS_MEyUQfdK0d_I1AlO9_v900Vx4nKpLheFQ__()