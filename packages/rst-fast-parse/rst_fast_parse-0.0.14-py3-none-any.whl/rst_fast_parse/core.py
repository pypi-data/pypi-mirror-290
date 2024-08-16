from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.elements import BasicElementList, ElementListProtocol, ElementProtocol
from rst_fast_parse._vwxyz import gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__

class gAAAAABmvnuPraSvzPr_j2lP7deGTfZusFG7XOVfOBNt_WXSsl_7CxjK1L5ZQh7lRtszllDG4Rb8iUhMCWjDhTgtHlDbOeqrWw__:

    def __init__(self, block_parsers: Sequence[gAAAAABmvnuPsGM2N7BzhSpAJ4ShmB9527600aR_Sm4bnf_46D_7K2xO2V293V23tbqlN3JGzdrf4jR4QM4B1I3pcvIfERU2UQ__], *, gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__: bool=True) -> None:
        self._gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__ = gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__
        self._block_parsers = block_parsers

    @property
    def gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__(self) -> bool:
        return self._gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__

    def gAAAAABmvnuP1xGGXxJqT1pfMi4mIQNM9cFfIkkaZzBImIH71vNciJqvJLG7qLWSoGxwzKZ_JLM8n7nUNPlyhKcmdxFhyzyXXQ__(self, source: gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__) -> tuple[ElementListProtocol, DiagnosticList]:
        end_of_file = False
        parent = BasicElementList()
        diagnostics: list[Diagnostic] = []
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuP_ClUFKNcZK3izoScss_N4ceBj9LXWkx42Msjc8XGvV8pQ0jcSFPd7BXVi3Qh2svvdS7_7MW5pdxsyUOXMvFZBw__:
                    break
                elif result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuPMhZZtYqBwgmlntAnk2pNEzm4IuBVbAOgcNUNPk5cwtS0ORGVXbj_bY3x708WqH8FacqCobgWvhXy_PI3HCP44A__:
                    continue
                elif result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuPRbdlsfvazMgv6xfcLvNC0QmLZyLevZAFSsO0gN3crEdWh85I5fK4AkyiRNRbEPJDXyQKddWPenhSD_uYCxVoJg__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmvnuPp_QE9_WnXWVDZg5oKVJ6LQ5CVrdrh1cxtPKUkZZB8K9_AZTE7wd9z5Ah21eEusDJcgxVmRcYg1wa0BtlMgWtfg__()
            if source.gAAAAABmvnuP_NyvWLXuPTynPoBgAgpfh2GFIrsxNt6Ti83oVtycTPZoLd0WhBfhHqSW36bezgc8VunqH1vm5wdq70EKy_VnYg__:
                break
        return (parent, diagnostics)

    def gAAAAABmvnuP1hvd_xfelN0N_WmyWGU1_7YIza4ZHl1631JbvqrNe9vLA3R6rrcW__PCVWxVAPdE_I6Bm2Bj4BwrOaODaF5DrQ__(self, source: gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__, parent: gAAAAABmvnuPPyMQkQupnqgLmhaaFYgOZLGB_6PmYhq6Z7EFG7fvQIeBKPWZau_qy3_gK97GQaP9Y21Bt9xfJC2if5OtnVuBGw__, diagnostics: gAAAAABmvnuPFiNsglZcNLAYt_CC2O1ysbl1SSMD2FRbUir08R6GhJ4_pHfdyZfFLoDODeMiuyT4FlxtDHsHs7Ap_zeSPfIJEoFJExTwUxoIYnI_IhBKuSQ_, /) -> None:
        old_gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__ = self._gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__
        try:
            self._gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuP_ClUFKNcZK3izoScss_N4ceBj9LXWkx42Msjc8XGvV8pQ0jcSFPd7BXVi3Qh2svvdS7_7MW5pdxsyUOXMvFZBw__:
                        break
                    elif result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuPMhZZtYqBwgmlntAnk2pNEzm4IuBVbAOgcNUNPk5cwtS0ORGVXbj_bY3x708WqH8FacqCobgWvhXy_PI3HCP44A__:
                        continue
                    elif result == gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_.gAAAAABmvnuPRbdlsfvazMgv6xfcLvNC0QmLZyLevZAFSsO0gN3crEdWh85I5fK4AkyiRNRbEPJDXyQKddWPenhSD_uYCxVoJg__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmvnuPYx_1AJ_ZlGlgvDrehH2B_nIHaCPrE9fnl6NCy1IGzbJUFbt_A6ls0oN30yko4kcNJOnUTmBis7jsENh0h5ePEw__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmvnuPp_QE9_WnXWVDZg5oKVJ6LQ5CVrdrh1cxtPKUkZZB8K9_AZTE7wd9z5Ah21eEusDJcgxVmRcYg1wa0BtlMgWtfg__()
                if source.gAAAAABmvnuP_NyvWLXuPTynPoBgAgpfh2GFIrsxNt6Ti83oVtycTPZoLd0WhBfhHqSW36bezgc8VunqH1vm5wdq70EKy_VnYg__:
                    break
        finally:
            self._gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__ = old_gAAAAABmvnuPCT19slLiOEo4irdY0Yol9kQHU8M6Oa7IKtDeDcRyv5CzhYZzK4W2euFuOuiE1mDvoOXro8oNGyWcaKI_msSjXw__

class gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_(Enum):
    gAAAAABmvnuP_ClUFKNcZK3izoScss_N4ceBj9LXWkx42Msjc8XGvV8pQ0jcSFPd7BXVi3Qh2svvdS7_7MW5pdxsyUOXMvFZBw__ = 0
    'The parser successfully matched the input.'
    gAAAAABmvnuPMhZZtYqBwgmlntAnk2pNEzm4IuBVbAOgcNUNPk5cwtS0ORGVXbj_bY3x708WqH8FacqCobgWvhXy_PI3HCP44A__ = 1
    'The parser did not match the input.'
    gAAAAABmvnuPRbdlsfvazMgv6xfcLvNC0QmLZyLevZAFSsO0gN3crEdWh85I5fK4AkyiRNRbEPJDXyQKddWPenhSD_uYCxVoJg__ = 2
    'The parser reached the end of the file.'

class gAAAAABmvnuPPyMQkQupnqgLmhaaFYgOZLGB_6PmYhq6Z7EFG7fvQIeBKPWZau_qy3_gK97GQaP9Y21Bt9xfJC2if5OtnVuBGw__(Protocol):

    def append(self, element: ElementProtocol) -> None:
        pass

class gAAAAABmvnuPFiNsglZcNLAYt_CC2O1ysbl1SSMD2FRbUir08R6GhJ4_pHfdyZfFLoDODeMiuyT4FlxtDHsHs7Ap_zeSPfIJEoFJExTwUxoIYnI_IhBKuSQ_(Protocol):

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmvnuPsGM2N7BzhSpAJ4ShmB9527600aR_Sm4bnf_46D_7K2xO2V293V23tbqlN3JGzdrf4jR4QM4B1I3pcvIfERU2UQ__(Protocol):

    def __call__(self, source: gAAAAABmvnuP_quFKpuYPWz7QdJ1kBaRmIwCQe9rCmHuVZv5Jk1eR82v8o4s8FimCtSYne_H63sWt2aoyl93LrLoAS2foR6HAA__, parent: gAAAAABmvnuPPyMQkQupnqgLmhaaFYgOZLGB_6PmYhq6Z7EFG7fvQIeBKPWZau_qy3_gK97GQaP9Y21Bt9xfJC2if5OtnVuBGw__, diagnostics: gAAAAABmvnuPFiNsglZcNLAYt_CC2O1ysbl1SSMD2FRbUir08R6GhJ4_pHfdyZfFLoDODeMiuyT4FlxtDHsHs7Ap_zeSPfIJEoFJExTwUxoIYnI_IhBKuSQ_, context: gAAAAABmvnuPraSvzPr_j2lP7deGTfZusFG7XOVfOBNt_WXSsl_7CxjK1L5ZQh7lRtszllDG4Rb8iUhMCWjDhTgtHlDbOeqrWw__, /) -> gAAAAABmvnuPNj42qdtIY8ySbUt8SHVpmQrQOLSobwLPYoj3RvNC1jY9pcO0EYhdFzdD_cMsPYESBwfRJcjrzDXWF59zSMUltg2pgUJdIA6tNFRc2rxItPQ_:
        pass