from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

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
    def gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__(self) -> bool:
        return not self._content.strip()

    def gAAAAABmuydMLffK9TxAiQCCgFGZzzyLgSbRMRoVemkdvFMa7m4tC63EaLu9_2CX4FsnJJHn4efh0H6iRhuPY1EWh6aDwFWl_g__(self) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        return gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__([self])

    def gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
        return gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmuydM2BDt_r61D8NjBMPiJlzEn_Pveo7_lZK90qmJvhl0apamolwKQjaXmXNUN5qaZFRGY1aPhpoo3iDtY9jdRHgEgg__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmuydMuxingcmOV5T6iiIllfz9fzMp1smuPNfmmBzxmavMK8vAvp6ljsp9gEO2LnZsgxyoyH07lZ_TjQ6SvzdB7sAZVw__(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmuydMXfz1AIWsDgOdvVKP_SILNaxE0ylZV_A_akbaeqa_npXrVtV5E2u50LBGu_ktj_Zi_MsSX26YZl_W2zZEZNSEYA__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def gAAAAABmuydMQMQdzY2n1tHKrwRTsUpxiPW2OqqLP9eBf7KORpmwkwSvf9RABCuoG0k0bcLTcCHDp_KM3j6YRj2bl5gKP8r_sA__(self) -> int:
        return self._current

    def gAAAAABmuydM3NOsP8_2N_P1DhbJSfRKMpm8xz4o9uW1S9A5rgppUUk4eOd9MT4pm1aHwvBrbp7GuicEAJRd9X4Y61XkFnXwpTdmBwHvGeMvatPvcegjz5g_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__(self) -> None | gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmuydMMDFHabcSdIh9mauc3_cVL_vPmICOToRMyXe24NJkI8PyaMKTQge2_LiSPcI2oRpWHdyIgMadE8ZUyD8xCSnCKQ__(self) -> None | gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmuydMPlSfgmYqlXEaJj4C82lAXKX89P7rqaNLHrOkC0Vlq5ViJ4MOUw1laSnp4veTcGvRCoXfpY9TrO3ccwvzqBEoCA__(self) -> Iterable[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__]:
        return iter(self._lines[self._current:])

    def gAAAAABmuydMjbS8YuuKhsP69b_LVvC78esxs5XU17tNBvFT5M78twv9zAr2BCdXDlxxlpryRxHeuS9otaesRd8zMuXC_yzrRg__(self, n: int=1) -> None | gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmuydMPNXekMCrPsz_vYOvYDs9_oPrgnfp3HgByoOHnDM0959v7DsbYZ6_m4qeg67gi4pyB8POEdOStAS6ZKU5A8yuhQ__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmuydMgGp1zxtMB3LqMXtilFCkg9VkTI4wy3_bYLi0JBOEylSKJahQoLf6NZZxDp0hhstN65CoqNG1cXLcS5Y3vvQntg__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmuydMwUqSrP8Dhm8XQ4XNpTKP3xob2XQmiTZ_vf2cdN_3kQsZhmLkHutr0odWPxf2Q_rbv_5Hmt3fVg0Nmuj4nchoUA__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        new_lines: list[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmuydMPhu3bjcxfpJErjVkmOmYO7VjGAHqilwD_n_R3_xZRE5HVpq_nU5WWLz5ZhlfNjQnlGrQk8ss2aCJsh9b3i5ycaxUC_bui7uGamDwIEa92FI_(self, *, start: bool=True, end: bool=True) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmuydMeG0hgXWowqZDBrK3GIr_iBS3mKGvvD5itqdCnJr8NiDgtT5SOYFokMh4CoB7XwJOQBtPGZ7fZpwoGRY7zA2ktA__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        new_lines: list[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuydMIjUaLCsHUadwbNK0codi6IPluaYq5pPNXqbH0cxWRrhw5_E_XFjiP9b3k40ibEIpJ1C9U_nS0DRlXKOa1X7xTA__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__, int | None]]:
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

    def gAAAAABmuydMzqlXDQIgcYwQHlQqmKtmcLSbgp_N7imSAujgY7zR6wtgIaxzgvfG8vbIWgmNetIxu_Jj3NzAsIuhKliFCND0LA__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        new_lines: list[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuydMIjUaLCsHUadwbNK0codi6IPluaYq5pPNXqbH0cxWRrhw5_E_XFjiP9b3k40ibEIpJ1C9U_nS0DRlXKOa1X7xTA__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuydMYWGOiYMRJte2AIZmsTpE5T8M9dIG1126Umz8TRob4u_BOar5DbSoFetNDDhxxWklCW_tXtv5uahJjW5xiumYvoH9Ov5G2wj8XFPVuaa51dk_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuydMIjUaLCsHUadwbNK0codi6IPluaYq5pPNXqbH0cxWRrhw5_E_XFjiP9b3k40ibEIpJ1C9U_nS0DRlXKOa1X7xTA__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(min_indent) for line in new_lines]
        if self.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__ is not None:
            new_lines.insert(0, self.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmuydMPhu3bjcxfpJErjVkmOmYO7VjGAHqilwD_n_R3_xZRE5HVpq_nU5WWLz5ZhlfNjQnlGrQk8ss2aCJsh9b3i5ycaxUC_bui7uGamDwIEa92FI_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmuydMPb4zkoCha1wtvezhuTDuxHI2YICB74Hxj5Jlmvh7ZnaoG1W5zx1zk2cZ6NUVogPUDJzx4RwHWMMlD1ChT0MtPMjaO2yl0B1NHRbzkvKzG6A_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmuydMXewr3wJ9aJ_2oIUAd34ETU2PfImZCzr9dibAm1dDUhVjXqrLNQa6EyIEe9o4Jt2ZoVKep67m4IX1R_dzZ0qHTA__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__):
                new_lines.append(line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmuydMIA0LSLzqw0txEKH3s3l7DiurA_YCUndDfzUr4FO5oo_5OcOoNHNxYlRgFct6oxOZ4lOYNxxYoZ4By4r46EDGaw__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmuydMPhu3bjcxfpJErjVkmOmYO7VjGAHqilwD_n_R3_xZRE5HVpq_nU5WWLz5ZhlfNjQnlGrQk8ss2aCJsh9b3i5ycaxUC_bui7uGamDwIEa92FI_(start=True, end=False)