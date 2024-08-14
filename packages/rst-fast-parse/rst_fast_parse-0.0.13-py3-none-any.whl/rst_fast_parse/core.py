from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.elements import BasicElementList, ElementBase, ElementListBase
from rst_fast_parse.source import gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__

class gAAAAABmuzW5IG2DIOzFQ2_BgRerOs8pBVI1raxL31rScqHbDhbX2TyFyfHE4BnBKJ4GkcLq7O85_42WmTHR8CZM4zUvLuwC3A__:

    def __init__(self, block_parsers: Sequence[gAAAAABmuzW5KF6JTBeA7QgAllsvQ7ypDP8CYQ830g1899Zvv7UE_POpZB4LPiJCu4n2GAllJKoXxaI6hviEC3QvETdYufnIZw__], *, gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__: bool=True) -> None:
        self._gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__ = gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__
        self._block_parsers = block_parsers

    @property
    def gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__(self) -> bool:
        return self._gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__

    def gAAAAABmuzW5GXZPW_H3HexjGyIo_M_2uSQQDuNp15tyQS0mmljr3E1OzJgxJbzVfLOhv6TlLss_CtdolM7okuTzwddnZbQn_A__(self, source: gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__) -> tuple[ElementListBase, DiagnosticList]:
        end_of_file = False
        parent = BasicElementList()
        diagnostics: list[Diagnostic] = []
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5cGW1dGZZqFeGZBKuf2ix3t1vYzrrgiuxxsZvJNPHCIxwNnoMUe9G6knvZI73Q7vQTNBFDEVy1RDfYYlJewOZnA__:
                    break
                elif result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5WchQQdt_CH6xXtPLfUXAzFfLwE_zd66Jn9DxdokAieVR_SGmH5vctL4SHHN1LppvzUwRVe8WAXsmYauX2bOYeQ__:
                    continue
                elif result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW51g7or_JrHPDhALqTLKWKEgWLGnshXnWk5pE9HSX17VZb0By6c4Sw0MNGPB90tcngphqyjQG3LZ87HEfzTEtqyw__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmuzW5_fx4nzCN_Dz_ns1I0OyUZLDKsz2zsq4fcjo6FuKDMKqYMVh_1y2LdG1kkh7bogqL0boAfJ6nZciiGuSI_dPv3A__()
            if source.gAAAAABmuzW55OMMebI70anEr6xTTXQpJyCPKUElQjPQ_NnJwOsqlkJFPK5pOQChq83QLSnEeeUsw0XP1vgEaG33tp0IPRqMrw__:
                break
        return (parent, diagnostics)

    def gAAAAABmuzW5SIZ92GvpNJwISfK4rOaQedVeA6IbwtQP8njKo9F_vS33C8UimJ2NcfEQ3hhsiTutppLesENYX0r_GoFIeZgYLw__(self, source: gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__, parent: gAAAAABmuzW5YBvbq__kiwx7eX1JpvJogwwOKOrI2LNS9hN3n1rRENfXGtK_vKjKDj_JWLIYu_LQjW0BkutMWFDZaM0hRjfHnw__, diagnostics: gAAAAABmuzW5wP2JFPpMIWlEZ_yZJ0YhVu3_cTccl16oao2owxf5LlR_ZIG_C1jl5MnmNvrJKdAkYYp2xtEgfvr3WwNaG6Lh8U921BWDoPcGRxlKz7UGkjI_, /) -> None:
        old_gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__ = self._gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__
        try:
            self._gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5cGW1dGZZqFeGZBKuf2ix3t1vYzrrgiuxxsZvJNPHCIxwNnoMUe9G6knvZI73Q7vQTNBFDEVy1RDfYYlJewOZnA__:
                        break
                    elif result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5WchQQdt_CH6xXtPLfUXAzFfLwE_zd66Jn9DxdokAieVR_SGmH5vctL4SHHN1LppvzUwRVe8WAXsmYauX2bOYeQ__:
                        continue
                    elif result == gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW51g7or_JrHPDhALqTLKWKEgWLGnshXnWk5pE9HSX17VZb0By6c4Sw0MNGPB90tcngphqyjQG3LZ87HEfzTEtqyw__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmuzW5_fx4nzCN_Dz_ns1I0OyUZLDKsz2zsq4fcjo6FuKDMKqYMVh_1y2LdG1kkh7bogqL0boAfJ6nZciiGuSI_dPv3A__()
                if source.gAAAAABmuzW55OMMebI70anEr6xTTXQpJyCPKUElQjPQ_NnJwOsqlkJFPK5pOQChq83QLSnEeeUsw0XP1vgEaG33tp0IPRqMrw__:
                    break
        finally:
            self._gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__ = old_gAAAAABmuzW5pwtQbj4CkHrd3vtFqjuQrJ0WWjtpqoJhrIBG9Yv7uN_fiwy5WmHgfkWWjQzLTrtdwTbcXifNdXnKqoaQONgn6g__

class gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_(Enum):
    gAAAAABmuzW5cGW1dGZZqFeGZBKuf2ix3t1vYzrrgiuxxsZvJNPHCIxwNnoMUe9G6knvZI73Q7vQTNBFDEVy1RDfYYlJewOZnA__ = 0
    'The parser successfully matched the input.'
    gAAAAABmuzW5WchQQdt_CH6xXtPLfUXAzFfLwE_zd66Jn9DxdokAieVR_SGmH5vctL4SHHN1LppvzUwRVe8WAXsmYauX2bOYeQ__ = 1
    'The parser did not match the input.'
    gAAAAABmuzW51g7or_JrHPDhALqTLKWKEgWLGnshXnWk5pE9HSX17VZb0By6c4Sw0MNGPB90tcngphqyjQG3LZ87HEfzTEtqyw__ = 2
    'The parser reached the end of the file.'

class gAAAAABmuzW5YBvbq__kiwx7eX1JpvJogwwOKOrI2LNS9hN3n1rRENfXGtK_vKjKDj_JWLIYu_LQjW0BkutMWFDZaM0hRjfHnw__(Protocol):

    def append(self, element: ElementBase) -> None:
        pass

class gAAAAABmuzW5wP2JFPpMIWlEZ_yZJ0YhVu3_cTccl16oao2owxf5LlR_ZIG_C1jl5MnmNvrJKdAkYYp2xtEgfvr3WwNaG6Lh8U921BWDoPcGRxlKz7UGkjI_(Protocol):

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmuzW5KF6JTBeA7QgAllsvQ7ypDP8CYQ830g1899Zvv7UE_POpZB4LPiJCu4n2GAllJKoXxaI6hviEC3QvETdYufnIZw__(Protocol):

    def __call__(self, source: gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__, parent: gAAAAABmuzW5YBvbq__kiwx7eX1JpvJogwwOKOrI2LNS9hN3n1rRENfXGtK_vKjKDj_JWLIYu_LQjW0BkutMWFDZaM0hRjfHnw__, diagnostics: gAAAAABmuzW5wP2JFPpMIWlEZ_yZJ0YhVu3_cTccl16oao2owxf5LlR_ZIG_C1jl5MnmNvrJKdAkYYp2xtEgfvr3WwNaG6Lh8U921BWDoPcGRxlKz7UGkjI_, context: gAAAAABmuzW5IG2DIOzFQ2_BgRerOs8pBVI1raxL31rScqHbDhbX2TyFyfHE4BnBKJ4GkcLq7O85_42WmTHR8CZM4zUvLuwC3A__, /) -> gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_:
        pass