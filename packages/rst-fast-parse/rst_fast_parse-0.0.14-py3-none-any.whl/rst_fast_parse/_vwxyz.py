from __future__ import annotations
import re
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

    @property
    def content(self) -> str:
        return self._content

    @property
    def line(self) -> int:
        return self._offset_line

    @property
    def indent(self) -> int:
        return self._offset_char

    @property
    def gAAAAABmvnuPPkZGuVG7rySsIzxg5qGN25cViT_kH2yqB1Jh4YgWuHYFeCggnKOC9aN7z3D2A8_1OQHaFV7ltGyYeMGtrldIWg__(self) -> bool:
        return not self._content.strip()

    def gAAAAABmvnuP7wTvl3_vbgF01e6sEFnZDFiVpxE6UBWGWXKbMAK0XjwS_JcmZMab_OPdzXmkvJ6sApYuRGMwlkEw0A_jW_UaQQ__(self) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        return gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__([self])

    def gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def gAAAAABmvnuPs9uixZfgbeHWXLeX9MNjmzX1in8i9jfmKOk8Ln_06dZQ8G4P8c_G_Y8kxDU4D7d_2prWoC0CjPNQ_1L2esaM_g__(self, n: int) -> gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        assert n >= 0
        new_offset = None if self._offset_char is None else self._offset_char + n
        return gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__(self._content[n:], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        return gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmvnuP_tQFcmakF_zIlg6ElAwckro80dLgllGVWR0jYrn_LFBghNPfwJwB4SJHRRQ8JbmrXDxc5ncPEduuRKCTg3Avzg__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmvnuP_NyvWLXuPTynPoBgAgpfh2GFIrsxNt6Ti83oVtycTPZoLd0WhBfhHqSW36bezgc8VunqH1vm5wdq70EKy_VnYg__(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmvnuP5vonXOqy6wNd496EOHIo5sjeX9t_ctOuutwUFnsZrTy0ol1Z2IpMgmfl92yb6f4dBlOEKMLMYOrHO2kBjvoiIw__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def gAAAAABmvnuP0zPXkwfEyPHZFnTDqXEbjurJgTKvkm_L5nKA1zVOregBsi3gY2qz7MAKfQmrvAep7aStFbZBurFOQQYT_7dtvQ__(self) -> int:
        return self._current

    def gAAAAABmvnuPajkyAEG4mSKsSUknMll1xcK9L0EodfiP9sfw1NfME107Rg5HolE_OD63ZAtwXJiFubWdBYvYhf0Oek6R45PKdtbBy247Lvg7VGID0YS8xCU_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__(self) -> None | gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmvnuPtSk5A9h7uoFTW9kQc_J179me2SXQYV0xfUAjl9qCaFt0mzEf2Um6Ld_aFscHpO2rxlifxEZAlIVBvvMQKO5aMg__(self) -> None | gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmvnuPc00Vq9J9c7__WyrXD66wbKtSeJyWZJP6V4KvFhRbjCxavOI3Yqf55kcufJFvpuAJIm7xBDSr4LxD_ZT76UhCUQ__(self) -> Iterable[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__]:
        return iter(self._lines[self._current:])

    def gAAAAABmvnuPuZXbXRIn_Z6uW7rl1b6tjkrw7FbiBfqZUZMylVWsCG9X6PO5txqGZgMgnn879eyop15Pa9oKq7BJnPqu2HDIpA__(self, n: int=1) -> None | gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmvnuPp_QE9_WnXWVDZg5oKVJ6LQ5CVrdrh1cxtPKUkZZB8K9_AZTE7wd9z5Ah21eEusDJcgxVmRcYg1wa0BtlMgWtfg__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmvnuPpiwYWIWH21eukoUsu8_dek_kurDmTm7MXy7hVTAfOZnzJUthCdp3ApDmUhoxh1lCcR9AN0Wo_pHiFBmaeEHHtA__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmvnuPuitFRunLAjfPGmxTYo7EoUVGkMDC8TEnYWWRJf5fCxlbqrS1OkLkbJ8rYzBGr8RfF_uDqtF7LQ7KJLw4meIjNQ__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        new_lines: list[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmvnuPPkZGuVG7rySsIzxg5qGN25cViT_kH2yqB1Jh4YgWuHYFeCggnKOC9aN7z3D2A8_1OQHaFV7ltGyYeMGtrldIWg__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmvnuPavqykqVbQIKiqX6moud9TFRqslmbfN8D1PtocINF4d8Xy4L_Wa0wWSvA0tg9Q545M_JnWotBnea4n1zS2vy2AFF5JJrvKU_5u7nP_S2vOQM_(self, *, start: bool=True, end: bool=True) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmvnuPPkZGuVG7rySsIzxg5qGN25cViT_kH2yqB1Jh4YgWuHYFeCggnKOC9aN7z3D2A8_1OQHaFV7ltGyYeMGtrldIWg__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmvnuPPkZGuVG7rySsIzxg5qGN25cViT_kH2yqB1Jh4YgWuHYFeCggnKOC9aN7z3D2A8_1OQHaFV7ltGyYeMGtrldIWg__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmvnuPf9ZlVJNO5okYogzW6u5Fj78rk6EKMlpWmi9wn5_8gsr1Jat0GPZQumQbhFuBub6MdhjzsVKnYaE1XCEfYPzCKA__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        new_lines: list[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmvnuPPkZGuVG7rySsIzxg5qGN25cViT_kH2yqB1Jh4YgWuHYFeCggnKOC9aN7z3D2A8_1OQHaFV7ltGyYeMGtrldIWg__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmvnuPtMsfyTPJUGPms4i9Fgda3KdxZCiPnzc8LyGyWT_fzkXKA2BVct9qKX9IlHCAJ7GDxdApMrJ8TaRqeouxrA8GGw__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__, int | None]]:
        for line in self._lines[self._current + offset:]:
            len_total = len(line.content)
            if line.content and line.content[0] != ' ':
                break
            len_indent = len_total - len(line.content.lstrip())
            only_whitespace = len_total == len_indent
            if until_blank and only_whitespace:
                break
            indent = None if only_whitespace else len_indent
            yield (line, indent)

    def gAAAAABmvnuPddP10VBKjmtudEfKvt2FR2gNt5Tco7ooMawvcp_XROSwb3HhODPvw0dtQP6l68b8ebFxcp6g8ZaPSM66N4xjEQ__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        new_lines: list[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmvnuPtMsfyTPJUGPms4i9Fgda3KdxZCiPnzc8LyGyWT_fzkXKA2BVct9qKX9IlHCAJ7GDxdApMrJ8TaRqeouxrA8GGw__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmvnuP7GYlBpyUMoBwe7_TunDc2_4uc29ah_BnEOCTXMP36oquCGO87r3iZjbChrmxPWCG4zdHc_1_NLP2mdqYNiLEPGwYP19x8fzhtNuYHwrbX00_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmvnuPtMsfyTPJUGPms4i9Fgda3KdxZCiPnzc8LyGyWT_fzkXKA2BVct9qKX9IlHCAJ7GDxdApMrJ8TaRqeouxrA8GGw__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(min_indent) for line in new_lines]
        if self.gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__ is not None:
            new_lines.insert(0, self.gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmvnuPavqykqVbQIKiqX6moud9TFRqslmbfN8D1PtocINF4d8Xy4L_Wa0wWSvA0tg9Q545M_JnWotBnea4n1zS2vy2AFF5JJrvKU_5u7nP_S2vOQM_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmvnuPOjFYx9CukvAlFG4IkqEY8TiMaHLiFnphgpaWKjU7jUp5Xmhfeb0JqIJIaOPP3ORvVlVsp416WYrX7EjjSluJWFGGzZQxh2oDHZzL9j05lhI_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmvnuP03gQQNO3ScydGRX_tclU8TA52qXEci0mmhhlXoCHle6xKY78ntnl4i3h5X0EgdalEzSeoh6nB7puR68YmzU_Og__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__):
                new_lines.append(line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmvnuPR2DVHMJKq4L1lTVtsGgt6K7nkBXbb_KimXG5OJbOHhZpih7msu54lksTH51MW3f3RSlZ58moN_ON4Lxv_JvgWg__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmvnuPavqykqVbQIKiqX6moud9TFRqslmbfN8D1PtocINF4d8Xy4L_Wa0wWSvA0tg9Q545M_JnWotBnea4n1zS2vy2AFF5JJrvKU_5u7nP_S2vOQM_(start=True, end=False)

def gAAAAABmvnuPxlKNyUpj8qlUoPHYlC2HuhJTfhie93SHnAaXOM_7jzWpUMbnPx6CW2E_rVLPS_U8_rBQFzjwkkYKlulOx33S6AhBPXLsz7ZgXQpgHoWaTu4_(text: str, *, tab_width: int=8, convert_whitespace: bool=True) -> list[str]:
    if convert_whitespace:
        text = re.sub('[\x0b\x0c]', ' ', text)
    return [s.expandtabs(tab_width).rstrip() for s in text.splitlines()]