from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.elements import BasicElementList, ElementBase, ElementListBase
from rst_fast_parse.source import gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__

class gAAAAABmuydMiLdU_dp59oVEPGBNv68vj5wG7_22Bvg5bZ03OT2G_QCzmRWERmHgVHtQYXo1mUcSENx4LswwbgB9jit4vTIw9A__:

    def __init__(self, block_parsers: Sequence[gAAAAABmuydMtmqQaUlCZC3V5hjKqkxx9csQRUj_mgRSUSqp9ECcAOmQtULRKUHk4iaztn7LuBruXi7Du_NqkYrCqLfoQgo23g__], *, gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__: bool=True) -> None:
        self._gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__ = gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__
        self._block_parsers = block_parsers

    @property
    def gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__(self) -> bool:
        return self._gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__

    def gAAAAABmuydMviZRBCvAA_Ra_womfSOKe6Sqk35acZmbv8ogNp_JDzdOtpgoiqExwDrer3ykWn3XWJiLVPyYHHA3_PAuIITpeQ__(self, source: gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__) -> tuple[ElementListBase, DiagnosticList]:
        end_of_file = False
        parent = BasicElementList()
        diagnostics: list[Diagnostic] = []
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydM_3nhN_OjUBfPISsOcE6uNx7vcMNK1buxeJMBIyldcdVwhb7nmW0jrIJL4sgbZgUGzuOO7yr8rsz0gqVTH3yLwg__:
                    break
                elif result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMKf1XPP798dMRx3PTLCDxb3oSW_v3i3TShC0b1ZBMlwGJvJcJxBiYfbIhB_70sjOifWGPv47p0bdjpiKqfq8JRA__:
                    continue
                elif result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMNoVXrdqJvzMnoVrlYn_r3Ve1p2VbhCA8q06J5yPCK6aa322xvsPFlWI_vQyJJvvsEyWZHSCuNOqhrJs9iswRJw__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmuydMPNXekMCrPsz_vYOvYDs9_oPrgnfp3HgByoOHnDM0959v7DsbYZ6_m4qeg67gi4pyB8POEdOStAS6ZKU5A8yuhQ__()
            if source.gAAAAABmuydMuxingcmOV5T6iiIllfz9fzMp1smuPNfmmBzxmavMK8vAvp6ljsp9gEO2LnZsgxyoyH07lZ_TjQ6SvzdB7sAZVw__:
                break
        return (parent, diagnostics)

    def gAAAAABmuydMMF7ZY53udCcS2ALzNb0Tz_DMP3IixR1JcbpUdl3ynb7luBKHkl8sLLd7on9MRLssGnahjwAivbf9MRBXSFHPbg__(self, source: gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__, parent: gAAAAABmuydMRweAvNUw6_RAhvNTsyROtSlhzkieQGDs7aJ4PmDgfnBl2w5qXfrC0rD9MRHqzLLKUy6bmJaLqiC8ueZoeMhy1g__, diagnostics: gAAAAABmuydMZvEEZ_3jzwR8q9BsCcTFE50XNDCYTKN1JJpJvt4d7iPcmxP85UNh63Bidy8VWJ_6TQqrL0uFnzCWChXUvr1w_sY_V65KaX_WzQiRcnhAjbk_, /) -> None:
        old_gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__ = self._gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__
        try:
            self._gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydM_3nhN_OjUBfPISsOcE6uNx7vcMNK1buxeJMBIyldcdVwhb7nmW0jrIJL4sgbZgUGzuOO7yr8rsz0gqVTH3yLwg__:
                        break
                    elif result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMKf1XPP798dMRx3PTLCDxb3oSW_v3i3TShC0b1ZBMlwGJvJcJxBiYfbIhB_70sjOifWGPv47p0bdjpiKqfq8JRA__:
                        continue
                    elif result == gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMNoVXrdqJvzMnoVrlYn_r3Ve1p2VbhCA8q06J5yPCK6aa322xvsPFlWI_vQyJJvvsEyWZHSCuNOqhrJs9iswRJw__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmuydMPNXekMCrPsz_vYOvYDs9_oPrgnfp3HgByoOHnDM0959v7DsbYZ6_m4qeg67gi4pyB8POEdOStAS6ZKU5A8yuhQ__()
                if source.gAAAAABmuydMuxingcmOV5T6iiIllfz9fzMp1smuPNfmmBzxmavMK8vAvp6ljsp9gEO2LnZsgxyoyH07lZ_TjQ6SvzdB7sAZVw__:
                    break
        finally:
            self._gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__ = old_gAAAAABmuydMJqfJa5tGPF9qe71EXXNkTvJmxV4jZC5Ame_U_SVas_LJGCnJw1Prkc6RnOAK6FwXGWoKgCaDEZZKdKJye7B_pQ__

class gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_(Enum):
    gAAAAABmuydM_3nhN_OjUBfPISsOcE6uNx7vcMNK1buxeJMBIyldcdVwhb7nmW0jrIJL4sgbZgUGzuOO7yr8rsz0gqVTH3yLwg__ = 0
    'The parser successfully matched the input.'
    gAAAAABmuydMKf1XPP798dMRx3PTLCDxb3oSW_v3i3TShC0b1ZBMlwGJvJcJxBiYfbIhB_70sjOifWGPv47p0bdjpiKqfq8JRA__ = 1
    'The parser did not match the input.'
    gAAAAABmuydMNoVXrdqJvzMnoVrlYn_r3Ve1p2VbhCA8q06J5yPCK6aa322xvsPFlWI_vQyJJvvsEyWZHSCuNOqhrJs9iswRJw__ = 2
    'The parser reached the end of the file.'

class gAAAAABmuydMRweAvNUw6_RAhvNTsyROtSlhzkieQGDs7aJ4PmDgfnBl2w5qXfrC0rD9MRHqzLLKUy6bmJaLqiC8ueZoeMhy1g__(Protocol):

    def append(self, element: ElementBase) -> None:
        pass

class gAAAAABmuydMZvEEZ_3jzwR8q9BsCcTFE50XNDCYTKN1JJpJvt4d7iPcmxP85UNh63Bidy8VWJ_6TQqrL0uFnzCWChXUvr1w_sY_V65KaX_WzQiRcnhAjbk_(Protocol):

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmuydMtmqQaUlCZC3V5hjKqkxx9csQRUj_mgRSUSqp9ECcAOmQtULRKUHk4iaztn7LuBruXi7Du_NqkYrCqLfoQgo23g__(Protocol):

    def __call__(self, source: gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__, parent: gAAAAABmuydMRweAvNUw6_RAhvNTsyROtSlhzkieQGDs7aJ4PmDgfnBl2w5qXfrC0rD9MRHqzLLKUy6bmJaLqiC8ueZoeMhy1g__, diagnostics: gAAAAABmuydMZvEEZ_3jzwR8q9BsCcTFE50XNDCYTKN1JJpJvt4d7iPcmxP85UNh63Bidy8VWJ_6TQqrL0uFnzCWChXUvr1w_sY_V65KaX_WzQiRcnhAjbk_, context: gAAAAABmuydMiLdU_dp59oVEPGBNv68vj5wG7_22Bvg5bZ03OT2G_QCzmRWERmHgVHtQYXo1mUcSENx4LswwbgB9jit4vTIw9A__, /) -> gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_:
        pass