from __future__ import annotations
from enum import Enum
from typing import Protocol, Sequence
from rst_fast_parse.diagnostics import Diagnostic, DiagnosticList
from rst_fast_parse.elements import BasicElementList, ElementBase, ElementListBase
from rst_fast_parse.source import gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__

class gAAAAABmuqBghF38b81pn__UU7D5qCVVFkK7i83u7DXAdQLWtiiS_ZydwaodSrj3IFh4yGUG6oGAUyeJMzZJr7WZ_UDS3ydTew__:

    def __init__(self, block_parsers: Sequence[gAAAAABmuqBgngnwpa_3UQFt_iToq6e806X5vBoW0gk5XgFZnSgj82E2eH4xhufLzoR9oh7SMmUakmycG923Q1IlIn03M4FHUg__], *, gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__: bool=True) -> None:
        self._gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__ = gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__
        self._block_parsers = block_parsers

    @property
    def gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__(self) -> bool:
        return self._gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__

    def gAAAAABmuqBgVLGuy_waSoTyJX8WOkQZqWJ6r3Gmo9z8aglauwZ6pf8IEHjIcYksqHSV3Gaa0Nxw32IBWSEinj5gK0Qme3oRuQ__(self, source: gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__) -> tuple[ElementListBase, DiagnosticList]:
        end_of_file = False
        parent = BasicElementList()
        diagnostics: list[Diagnostic] = []
        while not end_of_file:
            for parser in self._block_parsers:
                result = parser(source, parent, diagnostics, self)
                if result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBg1MYLqH2uc_9cl0kmH49d89xAylXzTxomRbGYuyr1699oUeyyGn48h7_rvDhj_neHQUhhf_8foQ0HA1D5HJ8gFw__:
                    break
                elif result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBgg3oVStjPL0fvHitctZj7GYy5hpgSVHhnqBN7CyhTVxkWOlO3n7cGwVyYiaVYSf_C2_eHOiD_4oxTBpabvZEUzg__:
                    continue
                elif result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBgKfbpVVNC7MvK1Dra1Alv7M5BtaEauTDfNX5IDsPJR0QSNUmfjdnymj3DP3ViTMNt2WDvxZfUcUqFyy_ZyAux5g__:
                    end_of_file = True
                    break
                else:
                    raise RuntimeError(f'Unknown parser result: {result!r}')
            else:
                if (line := source.gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__):
                    raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
            source.gAAAAABmuqBg_ATT7K3mNJmflzIxVvtzJZljH3kTQxBY15S3m14Zj9BkNcM0qDyapO3g7T50H8jNU0n8_AllJ90jHxBcb0OaVA__()
            if source.gAAAAABmuqBg21_mcE5SXy0rKj6Y_yN6aXZEX_Wy89P7NtgOPYhtwHYcjthRUo3Z_qq6MreEvDaSTl8sFstThyo7MVtbq0DN8Q__:
                break
        return (parent, diagnostics)

    def gAAAAABmuqBggT_j70GGTzkaIrvKFq65ggMKGob9Z_137Gwvo95SAWTSiVkPIKHpiMZvo9vLthsPv3V9qaRXwtGF3tP1bvhHzQ__(self, source: gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__, parent: gAAAAABmuqBgxYWrhw_rlzzYMMGWQOJhD2RaFKgPKB2wq9jzDEYBfwxTun6HdIi5h58FaJB1vYJmIXRekkKijRxFJSkGbhrtSg__, diagnostics: gAAAAABmuqBgi3FkS14lY3zFxXLMdRT3U_7FysMCGXu4_kVL2dSi7OnaSzLrCgWPKoqGI5fuLKI_xjZAPrs9YoYNMvPEB0_AzGK96yvqW_QAHyUvNasUB7I_, /) -> None:
        old_gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__ = self._gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__
        try:
            self._gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__ = False
            end_of_file = False
            while not end_of_file:
                for parser in self._block_parsers:
                    result = parser(source, parent, diagnostics, self)
                    if result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBg1MYLqH2uc_9cl0kmH49d89xAylXzTxomRbGYuyr1699oUeyyGn48h7_rvDhj_neHQUhhf_8foQ0HA1D5HJ8gFw__:
                        break
                    elif result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBgg3oVStjPL0fvHitctZj7GYy5hpgSVHhnqBN7CyhTVxkWOlO3n7cGwVyYiaVYSf_C2_eHOiD_4oxTBpabvZEUzg__:
                        continue
                    elif result == gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_.gAAAAABmuqBgKfbpVVNC7MvK1Dra1Alv7M5BtaEauTDfNX5IDsPJR0QSNUmfjdnymj3DP3ViTMNt2WDvxZfUcUqFyy_ZyAux5g__:
                        end_of_file = True
                        break
                    else:
                        raise RuntimeError(f'Unknown parser result: {result!r}')
                else:
                    if (line := source.gAAAAABmuqBgohObt0WbwaA8X_bW4_P4vs555AxepS7VQawstEi7wwQZwxVSLPyp3l8Ldxv3CSmUhuwzcjZjX25W1F0OwHE8Hg__):
                        raise RuntimeError(f'No parser matched line {line.line}: {line.content!r}')
                source.gAAAAABmuqBg_ATT7K3mNJmflzIxVvtzJZljH3kTQxBY15S3m14Zj9BkNcM0qDyapO3g7T50H8jNU0n8_AllJ90jHxBcb0OaVA__()
                if source.gAAAAABmuqBg21_mcE5SXy0rKj6Y_yN6aXZEX_Wy89P7NtgOPYhtwHYcjthRUo3Z_qq6MreEvDaSTl8sFstThyo7MVtbq0DN8Q__:
                    break
        finally:
            self._gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__ = old_gAAAAABmuqBgs_I26VV1A2HnaAL_iATcoqarumbRMLUIvVeZl74eH_DJMNAIivMcjgy_OqrK4aJ7DRLmRDaFGFXJmw_RrqmiRA__

class gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_(Enum):
    gAAAAABmuqBg1MYLqH2uc_9cl0kmH49d89xAylXzTxomRbGYuyr1699oUeyyGn48h7_rvDhj_neHQUhhf_8foQ0HA1D5HJ8gFw__ = 0
    'The parser successfully matched the input.'
    gAAAAABmuqBgg3oVStjPL0fvHitctZj7GYy5hpgSVHhnqBN7CyhTVxkWOlO3n7cGwVyYiaVYSf_C2_eHOiD_4oxTBpabvZEUzg__ = 1
    'The parser did not match the input.'
    gAAAAABmuqBgKfbpVVNC7MvK1Dra1Alv7M5BtaEauTDfNX5IDsPJR0QSNUmfjdnymj3DP3ViTMNt2WDvxZfUcUqFyy_ZyAux5g__ = 2
    'The parser reached the end of the file.'

class gAAAAABmuqBgxYWrhw_rlzzYMMGWQOJhD2RaFKgPKB2wq9jzDEYBfwxTun6HdIi5h58FaJB1vYJmIXRekkKijRxFJSkGbhrtSg__(Protocol):

    def append(self, element: ElementBase) -> None:
        pass

class gAAAAABmuqBgi3FkS14lY3zFxXLMdRT3U_7FysMCGXu4_kVL2dSi7OnaSzLrCgWPKoqGI5fuLKI_xjZAPrs9YoYNMvPEB0_AzGK96yvqW_QAHyUvNasUB7I_(Protocol):

    def append(self, diagnostic: Diagnostic) -> None:
        pass

class gAAAAABmuqBgngnwpa_3UQFt_iToq6e806X5vBoW0gk5XgFZnSgj82E2eH4xhufLzoR9oh7SMmUakmycG923Q1IlIn03M4FHUg__(Protocol):

    def __call__(self, source: gAAAAABmuqBgb_ur9sqdhNZkzGBHUGvU7Nfny0poOiJkTqM24EfSM_oxVkny_hL1SzzD4iWFrF9wC2pXcy0ZG_sJ9_k1fHTTNA__, parent: gAAAAABmuqBgxYWrhw_rlzzYMMGWQOJhD2RaFKgPKB2wq9jzDEYBfwxTun6HdIi5h58FaJB1vYJmIXRekkKijRxFJSkGbhrtSg__, diagnostics: gAAAAABmuqBgi3FkS14lY3zFxXLMdRT3U_7FysMCGXu4_kVL2dSi7OnaSzLrCgWPKoqGI5fuLKI_xjZAPrs9YoYNMvPEB0_AzGK96yvqW_QAHyUvNasUB7I_, context: gAAAAABmuqBghF38b81pn__UU7D5qCVVFkK7i83u7DXAdQLWtiiS_ZydwaodSrj3IFh4yGUG6oGAUyeJMzZJr7WZ_UDS3ydTew__, /) -> gAAAAABmuqBgf1WI5Eny4t5bHCfoNLC5_Hbdh6ZKNtYw_vCVXVqlXlSGn7hVy1jgT_1dI5A5xPANjzTR1pG_GQReL5iOzyUKI6hqmw4L7uU_k4DNfqB4y_Q_:
        pass