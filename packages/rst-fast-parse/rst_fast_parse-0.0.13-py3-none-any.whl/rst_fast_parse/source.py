from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

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
    def gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__(self) -> bool:
        return not self._content.strip()

    def gAAAAABmuzW5Rpwn_GwqpbCd9UIjZMYUVc3GDIXrBMBqYDNmcYXSDDMTVlHLSa4xxqHTFJiX295qSVfkptresYCAp3K0AmU6DA__(self) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        return gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__([self])

    def gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
        return gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmuzW5CboEnM_IOqKy7STtBvO5syB2_y9Cfj1DFpmS_RyQUwvvgdAZrGj3MK7eqGnWZqg4IMr6xmPNcgEkKQ8zjVuuUA__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmuzW55OMMebI70anEr6xTTXQpJyCPKUElQjPQ_NnJwOsqlkJFPK5pOQChq83QLSnEeeUsw0XP1vgEaG33tp0IPRqMrw__(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmuzW5im0aKK_z3_9U4IWClYyP63_pIC_1mhyiizIadtaPtfoeomlVlSZdE5XEvmqZJwPCmtiTl7kVXg9soEcD7cCnbA__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def gAAAAABmuzW58nNYLo9YpJF509bcPqw2vaGBdCds8CZcqzaDZ2BrYAl6GZEUR5kVKLUqTjIcJcPKLo8b5iSNNkVwxy6c9C0Ezg__(self) -> int:
        return self._current

    def gAAAAABmuzW57XRAWSq7MOHWcCmuENaKiZJbkL_bMY6f8FxaVRjyGp3ymRu4lo6h_iXplNkWfKHMVSvVTEtbH8LIc0Rvn4WMVv_31cxcOQBvdFmplZUZVqU_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__(self) -> None | gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmuzW57YBA6kEZTMNT3pHPGNkEU4ljWuGfgjFdXcCBN2X3GIuLUK7G1_DDF7NHf0fT9QTt7eCEmbhs8Yt24n_NS7mWtQ__(self) -> None | gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmuzW5b5hEsg9GLwqelmnY__kZgSvCTzAKNZ712P4PCDhtCc90ACWHOXIOz2AAXB63Z5iKG_4x_8fXEU3ySHf1iPv8TA__(self) -> Iterable[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__]:
        return iter(self._lines[self._current:])

    def gAAAAABmuzW5V_8liTKv0x_7_AsAe5dRzIzNyV7Bt3kjmR9HcO0sYrIbcg4M7ObjtIk7j0ADSJuTQELMH8Bojbj2S4umRjNcVw__(self, n: int=1) -> None | gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmuzW5_fx4nzCN_Dz_ns1I0OyUZLDKsz2zsq4fcjo6FuKDMKqYMVh_1y2LdG1kkh7bogqL0boAfJ6nZciiGuSI_dPv3A__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmuzW5Y3j7pfRA5QeJbYQcl5X7Gi_tPY25APtvn0FI_c8HWSO5fQXq_J9eu4XWl_x_onTUei0jWw7r8ZFogPHdMZdFtA__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmuzW5PKaORuUT7ekdmq319fsAb_E56BEoXfEFIHXFo5mGpGZHeMVjWvDS2uQ_wgMj3pB1_9IpvAyp35pkRQ1RLXhqmg__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        new_lines: list[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmuzW59USiaDOc_9kghOrFGWZwt6B7EBH6716JPoLmKRLLDwcsWHbYp60bIchrAsm7ohScGqvP7xFqCGiWqis_zOPvt2pW47yT8skV4tguB75F3d8_(self, *, start: bool=True, end: bool=True) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmuzW5iHwLzcMvV8xDqncFhQtSJckhu8Q4pG60cphVf01UKLqw37TZuLzLb_3Tcb4xg2Agj52JXyclTCNsqTztgHBRsg__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        new_lines: list[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuzW5T3wE0PSRQf2FxW0JXyWsx55mjNpG7djLFIegZFONF_NZs8ZGeqpTzGGB64I6vMrN6IB4mYlJYIzI64RWIPmd8Q__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__, int | None]]:
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

    def gAAAAABmuzW5w7u3ardXRnuMqV7OdFJW7Dmmu_X1_Y2JFtDmVf_i5mC0JUJoRBp2nzlFf4m1fbJ5S6saFVldbBfTT0ENYRd5tw__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        new_lines: list[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuzW5T3wE0PSRQf2FxW0JXyWsx55mjNpG7djLFIegZFONF_NZs8ZGeqpTzGGB64I6vMrN6IB4mYlJYIzI64RWIPmd8Q__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuzW5u0OstgF65lmACD5053iYy8yidhBXLPL1WN8IR5qWNy1Y2iH5WuwC0NBCS6hf_v18jUvpLO2WMXNbLpWjzfIYg_nHmaZJn5_tnak4Yr_JkwY_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuzW5T3wE0PSRQf2FxW0JXyWsx55mjNpG7djLFIegZFONF_NZs8ZGeqpTzGGB64I6vMrN6IB4mYlJYIzI64RWIPmd8Q__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(min_indent) for line in new_lines]
        if self.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__ is not None:
            new_lines.insert(0, self.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmuzW59USiaDOc_9kghOrFGWZwt6B7EBH6716JPoLmKRLLDwcsWHbYp60bIchrAsm7ohScGqvP7xFqCGiWqis_zOPvt2pW47yT8skV4tguB75F3d8_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmuzW51GVT3o_0t6LOghvWzx7wcCEeq7yKxqQYj2ldhgBmodGNfobmhpFraZnFHC8okMztHdSSwBK8cQ2LLjV9_vBsbJFi7iTLd_nlHTZWeNgD7KY_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmuzW52rR_xDml1M4h9RKOjs7gQbH3sQbj5w9Jnw9A05gxVgnSTXDAQgHFRBdFDtg1TXqOli9_kHYFm_LZqHcNR_2W1w__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__):
                new_lines.append(line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmuzW5YKMW5S8MVnoTqx3Iy5NPgQ_P8Rpp0B_Ql5C_YKPscuyZ8lESBYwksrRZfA5WSIvJyhMP2dNrPqczdg3n_7DR2w__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmuzW59USiaDOc_9kghOrFGWZwt6B7EBH6716JPoLmKRLLDwcsWHbYp60bIchrAsm7ohScGqvP7xFqCGiWqis_zOPvt2pW47yT8skV4tguB75F3d8_(start=True, end=False)