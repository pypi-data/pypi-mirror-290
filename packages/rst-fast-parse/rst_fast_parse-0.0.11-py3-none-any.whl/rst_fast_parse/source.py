from __future__ import annotations
from typing import Iterable, NewType, Sequence
PositiveInt = NewType('PositiveInt', int)

class gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
    __slots__ = ('_content', '_source', '_offset_line', '_offset_char')

    def __init__(self, content: str, /, offset_line: int, offset_char: int, *, source: str | None=None) -> None:
        self._content = content
        self._source = source
        self._offset_line = offset_line
        self._offset_char = offset_char

    def __repr__(self) -> str:
        return f'gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__({self._content!r}, line={self._offset_line}, char={self._offset_char})'

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
    def gAAAAABmuqBgl4E5Lo3PT8VqK5GKvo4Ku32ltoCn3DAeeb5AORmj39SZqbyqaEAHS0iLZH8zwsxa1HKGpLo7TlFeHgYFLagNXQ__(self) -> bool:
        return not self._content.strip()

    def gAAAAABmuqBgaOHGS6lDMD6WpG7PAKCKhW6hSXEtcfJenfqaoJ_v5M41WnasxBd2OC3sOj_E2s08MXrq7F7oGYfPxp0o_rwnDA__(self) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        return gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__([self])

    def gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(self, /, start: PositiveInt | None, stop: None | PositiveInt=None) -> gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
        if self._offset_char is None:
            new_offset = None
        else:
            new_offset = self._offset_char + (start or 0)
        return gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__(self._content[start:stop], offset_line=self._offset_line, offset_char=new_offset, source=self._source)

    def rstrip(self) -> gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
        return gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__(self._content.rstrip(), offset_line=self._offset_line, offset_char=self._offset_char, source=self._source)

class gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
    __slots__ = ('_lines', '_current')

    def __init__(self, lines: Sequence[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__]) -> None:
        self._lines = lines
        self._current: int = 0
        'The current line index,\n\n        Note it can never be negative, but can be greater than the number of lines.\n        '

    def __repr__(self) -> str:
        return f'gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__(lines={len(self._lines)}, index={self._current})'

    def gAAAAABmuqBgfx318E2m8b55FGp7rQQZ0hKdgNLQlVx0btAO2L8kwP7JmWCDAPhRqQqZ8Q4CQm_g9J4jVPL0tcNb6WUekzQOgw__(self, *, newline: str='\n') -> str:
        return newline.join((line.content for line in self._lines[self._current:]))

    @property
    def gAAAAABmuqBg21_mcE5SXy0rKj6Y_yN6aXZEX_Wy89P7NtgOPYhtwHYcjthRUo3Z_qq6MreEvDaSTl8sFstThyo7MVtbq0DN8Q__(self) -> bool:
        return not self._lines[self._current:]

    def gAAAAABmuqBgjo1jrogVCpw_yrmkHto2uzQV6wr5gC3NihujN401gqqiBJMy425Xam9n6Su0A1A3XmIwvBrF1qfk2C4hmwFMhw__(self) -> int:
        return len(self._lines[self._current:])

    @property
    def gAAAAABmuqBgkNGinoIT4nDyAF1_rxe_t3T2gq5ohF_4keqmZ02YreuRBhEpNVJNi08k_rOBWnLuzW1ZCg2EF9_Yg40hKrEkVQ__(self) -> int:
        return self._current

    def gAAAAABmuqBgzqbRUVAyLhCEfiSnLOq0RiPZd7Wp4xG9LYppizLIirOnm8h2RWPjKmThkWEv7zrFYe_A_ZKoC1Kfr6VR8n8amW6trY_BEDPd7uku9EYZ4wM_(self, index: int) -> None:
        self._current = index if index >= 0 else 0

    @property
    def gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__(self) -> None | gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
        try:
            return self._lines[self._current]
        except IndexError:
            return None

    @property
    def gAAAAABmuqBgfkBNr8Lkgy38MN4HxAyhGUh9Xhdq8bHGEJGudvDFQ48zyAuM4FCD1emHvCmSkIR9S4h0u_2CreuGS2pBFmWmYQ__(self) -> None | gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
        try:
            self._lines[self._current]
            return self._lines[-1]
        except IndexError:
            return None

    def gAAAAABmuqBgqCjOt5_Zbc1dDw5Q6PoiEUZ_zP0SyURWU5cwuX_WyExydsLJDxe2fjPNtymxcVDVyRWXyHAs_TDXHasPXrlZjw__(self) -> Iterable[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__]:
        return iter(self._lines[self._current:])

    def gAAAAABmuqBgw0qXQnkGD_Qskyuj3wpd_CG0dmMClRMYzgDtfudQYBezEq_WpYumEDfXZrbdJs4eQsgs8e4DIdu_9_6lKX9iQQ__(self, n: int=1) -> None | gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__:
        try:
            return self._lines[self._current + n]
        except IndexError:
            return None

    def gAAAAABmuqBg_ATT7K3mNJmflzIxVvtzJZljH3kTQxBY15S3m14Zj9BkNcM0qDyapO3g7T50H8jNU0n8_AllJ90jHxBcb0OaVA__(self, n: int=1) -> None:
        self._current += n

    def gAAAAABmuqBgmREbJy8vp9L2VClyu7NZCsXnqyt54Z56EQ06ng1kCoWK2BwiNsKaIbgWLdclDIbSErGyJYieLyRVY1bQ_yyekA__(self, n: int=1) -> None:
        self._current -= n
        if self._current < 0:
            self._current = 0

    def gAAAAABmuqBgFJIfJMVaspkvsCpnMsJ7v5MGuPM5jefiGEispjWqN8yaaf5fPKLYJg5E7DAz1JDxa6FHDNZ2ZfnhFkz9t1LE3g__(self, top_offset: int, bottom_offset: int | None, /, *, start_offset: PositiveInt | None=None, stop_offset: PositiveInt | None=None, strip_min_indent: bool=False) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        new_lines: list[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__] = []
        for line in self._lines[self._current + top_offset:None if bottom_offset is None else self._current + bottom_offset]:
            if start_offset is None and stop_offset is None:
                new_lines.append(line)
            else:
                new_lines.append(line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(start_offset, stop_offset))
        if strip_min_indent:
            indents = [len(line.content) - len(line.content.lstrip()) for line in new_lines if not line.gAAAAABmuqBgl4E5Lo3PT8VqK5GKvo4Ku32ltoCn3DAeeb5AORmj39SZqbyqaEAHS0iLZH8zwsxa1HKGpLo7TlFeHgYFLagNXQ__]
            if (min_indent := PositiveInt(min(indents, default=0))):
                new_lines = [line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(min_indent) for line in new_lines]
        return self.__class__(new_lines)

    def gAAAAABmuqBgLlcoEbMEEA2lULYJdwj1t9crWVkGo5MWdrr1zkgI7Ixgo_Y3URjb7iQMAPcLdb2d_1isVCR5Y3VaoJU8YPq6BqeL7FfgbU7MOiCh2sS1F_Q_(self, *, start: bool=True, end: bool=True) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        start_index = 0
        lines = self._lines[self._current:]
        end_index = len(lines)
        if start:
            for line in lines:
                if not line.gAAAAABmuqBgl4E5Lo3PT8VqK5GKvo4Ku32ltoCn3DAeeb5AORmj39SZqbyqaEAHS0iLZH8zwsxa1HKGpLo7TlFeHgYFLagNXQ__:
                    break
                start_index += 1
        if end:
            for line in reversed(lines):
                if not line.gAAAAABmuqBgl4E5Lo3PT8VqK5GKvo4Ku32ltoCn3DAeeb5AORmj39SZqbyqaEAHS0iLZH8zwsxa1HKGpLo7TlFeHgYFLagNXQ__:
                    break
                end_index -= 1
        if end_index > start_index:
            return self.__class__(lines[start_index:end_index])
        else:
            return self.__class__([])

    def gAAAAABmuqBgbJMrruP3D7RNcmjr5tjSd_BTue9o4iWw711fV3_teZFcRX0iv8YazHZCoiSKfSCmEEYEUfVKh3x2bNHQ04_8tA__(self, *, stop_on_indented: bool=False, advance: bool=False) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        new_lines: list[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__] = []
        for line in self._lines[self._current:]:
            if line.gAAAAABmuqBgl4E5Lo3PT8VqK5GKvo4Ku32ltoCn3DAeeb5AORmj39SZqbyqaEAHS0iLZH8zwsxa1HKGpLo7TlFeHgYFLagNXQ__:
                break
            if stop_on_indented and line.content[0] == ' ':
                break
            new_lines.append(line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuqBgthN7obxFN4poOQOWIAqSHaJBKolYasgNphETFbQCM_xTlznWTBAEk9nCgbVCFv8Jel7_6vcX4YigpMsV1TtjZA__(self, offset: int, until_blank: bool, /) -> Iterable[tuple[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__, int | None]]:
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

    def gAAAAABmuqBgE8jYaaNMhhRmrPBzCbkv3xp5w7kPw7mpi5YBKhmhHsCKF9R9PfgW3RmRRnZWk59NUiq_O0UPisX3Mz8kCbw2eQ__(self, *, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        new_lines: list[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuqBgthN7obxFN4poOQOWIAqSHaJBKolYasgNphETFbQCM_xTlznWTBAEk9nCgbVCFv8Jel7_6vcX4YigpMsV1TtjZA__(0, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(min_indent) for line in new_lines]
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines)

    def gAAAAABmuqBgR6nkTuatlmEgSX35qeEX9yLxp_BhUDbMKFiwqSVwh1r9bn61FpKA4ZG_VNfojToT25ae1THlyoLKF8qF4WzPJ7DFIkuyrImgPgPNiaZa820_(self, *, first_indent: int=0, until_blank: bool=False, strip_indent: bool=True, strip_top: bool=True, strip_bottom: bool=False, advance: bool=False) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        first_indent = PositiveInt(first_indent)
        new_lines: list[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__] = []
        indents: list[int] = []
        for line, indent in self.gAAAAABmuqBgthN7obxFN4poOQOWIAqSHaJBKolYasgNphETFbQCM_xTlznWTBAEk9nCgbVCFv8Jel7_6vcX4YigpMsV1TtjZA__(1, until_blank):
            if indent is not None:
                indents.append(indent)
            new_lines.append(line)
        if strip_indent and indents:
            min_indent = PositiveInt(min(indents))
            new_lines = [line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(min_indent) for line in new_lines]
        if self.gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__ is not None:
            new_lines.insert(0, self.gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(first_indent))
        if new_lines and advance:
            self._current += len(new_lines) - 1
        block = self.__class__(new_lines)
        if strip_top or strip_bottom:
            return block.gAAAAABmuqBgLlcoEbMEEA2lULYJdwj1t9crWVkGo5MWdrr1zkgI7Ixgo_Y3URjb7iQMAPcLdb2d_1isVCR5Y3VaoJU8YPq6BqeL7FfgbU7MOiCh2sS1F_Q_(start=strip_top, end=strip_bottom)
        return block

    def gAAAAABmuqBg4Uy1Lo4cHcdPv5KdrsC83VAcBuaElrmaXYKhpw6I6Utta_P8nQIxKi1GdDhblMbAxY_p13TCxym16_AvxdvDG6B1rRv41Pb6qWa_Ml_FJUA_(self, indent: int, *, always_first: bool=False, until_blank: bool=False, strip_indent: bool=True, advance: bool=False) -> gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__:
        indent = PositiveInt(indent)
        new_lines: list[gAAAAABmuqBgvYPxYEjY1Dyef8YFjWw3eYQhfWlHzOZXeiStkLy25nQhXFSF0i7ofgHKHNaTD87Ci0Nx5_bGtegVgpfWoZxodg__] = []
        line_index = self._current
        if always_first:
            if (line := self.gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__):
                new_lines.append(line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(indent))
            line_index += 1
        for line in self._lines[line_index:]:
            len_total = len(line.content)
            len_indent = len_total - len(line.content.lstrip())
            if len_total != 0 and len_indent < indent:
                break
            if until_blank and len_total == len_indent:
                break
            new_lines.append(line.gAAAAABmuqBgsgHaluepAetP76ihXQjHqn4h5VwSq_71_uGkgCbCDS6VXguZdgkx4ve5OcqaTEqp4Bx3f6IJX3jfuAjWQHshLQ__(indent) if strip_indent else line)
        if new_lines and advance:
            self._current += len(new_lines) - 1
        return self.__class__(new_lines).gAAAAABmuqBgLlcoEbMEEA2lULYJdwj1t9crWVkGo5MWdrr1zkgI7Ixgo_Y3URjb7iQMAPcLdb2d_1isVCR5Y3VaoJU8YPq6BqeL7FfgbU7MOiCh2sS1F_Q_(start=True, end=False)