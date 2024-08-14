from __future__ import annotations
import re
from typing import Callable, Literal
from typing_extensions import TypeAlias
from rst_fast_parse.core import gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_, gAAAAABmuzW5IG2DIOzFQ2_BgRerOs8pBVI1raxL31rScqHbDhbX2TyFyfHE4BnBKJ4GkcLq7O85_42WmTHR8CZM4zUvLuwC3A__, gAAAAABmuzW5wP2JFPpMIWlEZ_yZJ0YhVu3_cTccl16oao2owxf5LlR_ZIG_C1jl5MnmNvrJKdAkYYp2xtEgfvr3WwNaG6Lh8U921BWDoPcGRxlKz7UGkjI_, gAAAAABmuzW5YBvbq__kiwx7eX1JpvJogwwOKOrI2LNS9hN3n1rRENfXGtK_vKjKDj_JWLIYu_LQjW0BkutMWFDZaM0hRjfHnw__
from rst_fast_parse.elements import ListElement, ListItemElement
from rst_fast_parse._hijklmn.pppppppp import gAAAAABmuzW5y5m2mpX5c9k1OPIJO1gEZ1kQCOeAxgVXb3CiGSdz_v1I2z8KYo_02sTLo1Nb1iIJjCRIYhIHXxk0FyT2xH1DSA__
from rst_fast_parse.source import gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__
from rst_fast_parse._opqrstu.tttttttt import gAAAAABmuzW5gDFBmAwGEYXDn1aLdrZpnRQtOorpkIh3khPF9F4eeCmZn1RvpUR9KMlwufBVzFASg2Kewu3XOaKJpk63uxGd9aUumScrsFk2ROVczssaLA8_
from rst_fast_parse._opqrstu.uuuuuuuu import gAAAAABmuzW5oBG14suyc2iIFboFLg3wGhmEkSudByNQqDbYUdkLtKmzz2nnEqMqQBJscQJg3soNKMn_HRTKSst3lJ_3_6N8_g__

def gAAAAABmuzW5wjzxNygbqs6DzYdaZjgu905A1H5_rRNjKSj32UC_UW4OtqAd5uK8zjtkndD2ksXh70hEWzxh3jxERGnWe5jRRQd__3kRHF38yaw6UkwTGp8_(source: gAAAAABmuzW5gCpc2iB7L_IZqccSZQ_JOuULzpLSGB9fPo5f5ersHwDKkzF5mqUG7hm539xIfRj2Ihpqun9d6ziBKqDfROoO9w__, parent: gAAAAABmuzW5YBvbq__kiwx7eX1JpvJogwwOKOrI2LNS9hN3n1rRENfXGtK_vKjKDj_JWLIYu_LQjW0BkutMWFDZaM0hRjfHnw__, diagnostics: gAAAAABmuzW5wP2JFPpMIWlEZ_yZJ0YhVu3_cTccl16oao2owxf5LlR_ZIG_C1jl5MnmNvrJKdAkYYp2xtEgfvr3WwNaG6Lh8U921BWDoPcGRxlKz7UGkjI_, context: gAAAAABmuzW5IG2DIOzFQ2_BgRerOs8pBVI1raxL31rScqHbDhbX2TyFyfHE4BnBKJ4GkcLq7O85_42WmTHR8CZM4zUvLuwC3A__, /) -> gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_:
    if (init_line := source.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__) is None:
        return gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW51g7or_JrHPDhALqTLKWKEgWLGnshXnWk5pE9HSX17VZb0By6c4Sw0MNGPB90tcngphqyjQG3LZ87HEfzTEtqyw__
    if (result := gAAAAABmuzW5EedEFUdxdzTH6mGf7b7n7GEN2iTUUAJumhekzB_BKuSQZItQxSJT3vP4DmP1t4q83_femq1IKtXNALxfTfgVNcKVs3Rdfh5nVtLZLGslsBk_(init_line.content)) is None:
        return gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5WchQQdt_CH6xXtPLfUXAzFfLwE_zd66Jn9DxdokAieVR_SGmH5vctL4SHHN1LppvzUwRVe8WAXsmYauX2bOYeQ__
    init_format, init_type, init_ordinal, _ = result
    last_auto = init_type == 'auto'
    last_ordinal: int | None = None
    if init_type == 'auto':
        init_type = 'arabic'
    if (next_line := source.gAAAAABmuzW5V_8liTKv0x_7_AsAe5dRzIzNyV7Bt3kjmR9HcO0sYrIbcg4M7ObjtIk7j0ADSJuTQELMH8Bojbj2S4umRjNcVw__()) and (not next_line.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__) and next_line.content[:1].strip() and (not gAAAAABmuzW5EedEFUdxdzTH6mGf7b7n7GEN2iTUUAJumhekzB_BKuSQZItQxSJT3vP4DmP1t4q83_femq1IKtXNALxfTfgVNcKVs3Rdfh5nVtLZLGslsBk_(next_line.content)):
        return gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5WchQQdt_CH6xXtPLfUXAzFfLwE_zd66Jn9DxdokAieVR_SGmH5vctL4SHHN1LppvzUwRVe8WAXsmYauX2bOYeQ__
    items: list[ListItemElement] = []
    while (gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__ := source.gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__):
        if gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.gAAAAABmuzW54ldaVHeDdTIEEdwkCXIjJLWNdorcjEv9vrhLUPJG2unpp0n6nGAD6M_gv06eFRzyU6_pdhZsav6Qg4TbvG6AZQ__:
            source.gAAAAABmuzW5_fx4nzCN_Dz_ns1I0OyUZLDKsz2zsq4fcjo6FuKDMKqYMVh_1y2LdG1kkh7bogqL0boAfJ6nZciiGuSI_dPv3A__()
            continue
        if (result := gAAAAABmuzW5EedEFUdxdzTH6mGf7b7n7GEN2iTUUAJumhekzB_BKuSQZItQxSJT3vP4DmP1t4q83_femq1IKtXNALxfTfgVNcKVs3Rdfh5nVtLZLGslsBk_(gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.content, init_type)) is not None:
            eformat, etype, next_ordinal, char_offset = result
            if eformat != init_format or (etype != 'auto' and (etype != init_type or last_auto or (last_ordinal is not None and next_ordinal != last_ordinal + 1))):
                source.gAAAAABmuzW5Y3j7pfRA5QeJbYQcl5X7Gi_tPY25APtvn0FI_c8HWSO5fQXq_J9eu4XWl_x_onTUei0jWw7r8ZFogPHdMZdFtA__()
                break
            if len(gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.content) > char_offset:
                content = source.gAAAAABmuzW51GVT3o_0t6LOghvWzx7wcCEeq7yKxqQYj2ldhgBmodGNfobmhpFraZnFHC8okMztHdSSwBK8cQ2LLjV9_vBsbJFi7iTLd_nlHTZWeNgD7KY_(char_offset, always_first=True, advance=True)
            else:
                content = source.gAAAAABmuzW5u0OstgF65lmACD5053iYy8yidhBXLPL1WN8IR5qWNy1Y2iH5WuwC0NBCS6hf_v18jUvpLO2WMXNbLpWjzfIYg_nHmaZJn5_tnak4Yr_JkwY_(first_indent=char_offset, advance=True)
            list_item = ListItemElement((gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.line, gAAAAABmuzW5AE8KnZXfPFKWsqQ3Ke0lVy4UA10kuV3H_Y_nrL2qS9hhJtYH5zDRJ1nh_s89eV3CP_pSkU0oTSuYsi823Q553g__.line if content.gAAAAABmuzW57YBA6kEZTMNT3pHPGNkEU4ljWuGfgjFdXcCBN2X3GIuLUK7G1_DDF7NHf0fT9QTt7eCEmbhs8Yt24n_NS7mWtQ__ is None else content.gAAAAABmuzW57YBA6kEZTMNT3pHPGNkEU4ljWuGfgjFdXcCBN2X3GIuLUK7G1_DDF7NHf0fT9QTt7eCEmbhs8Yt24n_NS7mWtQ__.line))
            items.append(list_item)
            context.gAAAAABmuzW5SIZ92GvpNJwISfK4rOaQedVeA6IbwtQP8njKo9F_vS33C8UimJ2NcfEQ3hhsiTutppLesENYX0r_GoFIeZgYLw__(content, list_item, diagnostics)
            last_auto = etype == 'auto'
            last_ordinal = next_ordinal
            source.gAAAAABmuzW5_fx4nzCN_Dz_ns1I0OyUZLDKsz2zsq4fcjo6FuKDMKqYMVh_1y2LdG1kkh7bogqL0boAfJ6nZciiGuSI_dPv3A__()
        else:
            source.gAAAAABmuzW5Y3j7pfRA5QeJbYQcl5X7Gi_tPY25APtvn0FI_c8HWSO5fQXq_J9eu4XWl_x_onTUei0jWw7r8ZFogPHdMZdFtA__()
            break
    if items:
        parent.append(ListElement('enum_list', items))
        gAAAAABmuzW5gDFBmAwGEYXDn1aLdrZpnRQtOorpkIh3khPF9F4eeCmZn1RvpUR9KMlwufBVzFASg2Kewu3XOaKJpk63uxGd9aUumScrsFk2ROVczssaLA8_(diagnostics, source, 'Enumerated list')
    return gAAAAABmuzW5kkhzBl9KcrTu9DtqyhuFYLd4zuTzdikHT5pmmFks6bsiR94QUguK6BhJ2ip4VN1aCf_kBHokOv147LBBlT6FOkaWlpRwOqP3PDIuh8bd1cM_.gAAAAABmuzW5cGW1dGZZqFeGZBKuf2ix3t1vYzrrgiuxxsZvJNPHCIxwNnoMUe9G6knvZI73Q7vQTNBFDEVy1RDfYYlJewOZnA__
_ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
_EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']
gAAAAABmuzW59HE_UN212d33ue4gKsb5NC5GhdjmD5rzEkoVHh6CUW9us7Pz6PFF8AriEsr_57GNG7Yq4cw8D5jTVXbL6CLuQvXRwbvbl61STmMc94Y_Xp0_: dict[_EnumType, tuple[str, _EnumType]] = {'auto': ('^[0-9]+$', 'arabic'), 'arabic': ('^[0-9]+$', 'arabic'), 'loweralpha': ('^[a-z]$', 'loweralpha'), 'upperalpha': ('^[A-Z]$', 'upperalpha'), 'lowerroman': ('^[ivxlcdm]+$', 'lowerroman'), 'upperroman': ('^[IVXLCDM]+$', 'upperroman')}
gAAAAABmuzW5J89XQJ3OUCWY8Dd_F9FyYtA28k2LFZ7YRYgyc_WhCaBUdNOzC33Qtl2vfUNUr1iw3WGWSgjrHNME5m6fvgDfaQ__: tuple[tuple[str, _EnumType], ...] = (('^[0-9]+$', 'arabic'), ('^[a-z]$', 'loweralpha'), ('^[A-Z]$', 'upperalpha'), ('^[ivxlcdm]+$', 'lowerroman'), ('^[IVXLCDM]+$', 'upperroman'))
gAAAAABmuzW5ulJOes7XE3JtL2SS35FfZ_xnhGpJHFl23X_XFP1hQBFGWddIJ_Du3l8HfgkQcSeqXb8NgS5Z7h7D8_mPaeRKJ1vSn6jJ1MZnrTO_hg9Nq78_: dict[_EnumType, Callable[[str], int | None]] = {'auto': lambda t: 1, 'arabic': int, 'loweralpha': lambda t: ord(t) - ord('a') + 1, 'upperalpha': lambda t: ord(t) - ord('A') + 1, 'lowerroman': lambda t: gAAAAABmuzW5oBG14suyc2iIFboFLg3wGhmEkSudByNQqDbYUdkLtKmzz2nnEqMqQBJscQJg3soNKMn_HRTKSst3lJ_3_6N8_g__(t.upper()), 'upperroman': lambda t: gAAAAABmuzW5oBG14suyc2iIFboFLg3wGhmEkSudByNQqDbYUdkLtKmzz2nnEqMqQBJscQJg3soNKMn_HRTKSst3lJ_3_6N8_g__(t)}

def gAAAAABmuzW5EedEFUdxdzTH6mGf7b7n7GEN2iTUUAJumhekzB_BKuSQZItQxSJT3vP4DmP1t4q83_femq1IKtXNALxfTfgVNcKVs3Rdfh5nVtLZLGslsBk_(line: str, expected: None | _EnumType=None) -> None | tuple[_ParenType, _EnumType, int, int]:
    if not (match := re.match(gAAAAABmuzW5y5m2mpX5c9k1OPIJO1gEZ1kQCOeAxgVXb3CiGSdz_v1I2z8KYo_02sTLo1Nb1iIJjCRIYhIHXxk0FyT2xH1DSA__, line)):
        return None
    fmt: _ParenType
    for fmt in ('parens', 'rparen', 'period'):
        if (submatch := match.group(fmt)):
            text: str = submatch[:-1]
            if fmt == 'parens':
                text = text[1:]
            break
    else:
        raise RuntimeError(f'enumerator format not matched: {line!r}')
    sequence: None | _EnumType = None
    if text == '#':
        sequence = 'auto'
    elif expected is not None:
        regex, result = gAAAAABmuzW59HE_UN212d33ue4gKsb5NC5GhdjmD5rzEkoVHh6CUW9us7Pz6PFF8AriEsr_57GNG7Yq4cw8D5jTVXbL6CLuQvXRwbvbl61STmMc94Y_Xp0_[expected]
        if re.match(regex, text):
            sequence = result
    elif text == 'i':
        sequence = 'lowerroman'
    elif text == 'I':
        sequence = 'upperroman'
    if sequence is None:
        for regex, result in gAAAAABmuzW5J89XQJ3OUCWY8Dd_F9FyYtA28k2LFZ7YRYgyc_WhCaBUdNOzC33Qtl2vfUNUr1iw3WGWSgjrHNME5m6fvgDfaQ__:
            if re.match(regex, text):
                sequence = result
                break
        else:
            raise RuntimeError(f'enumerator sequence not matched: {text!r}')
    if (ordinal := gAAAAABmuzW5ulJOes7XE3JtL2SS35FfZ_xnhGpJHFl23X_XFP1hQBFGWddIJ_Du3l8HfgkQcSeqXb8NgS5Z7h7D8_mPaeRKJ1vSn6jJ1MZnrTO_hg9Nq78_[sequence](text)) is None:
        return None
    return (fmt, sequence, ordinal, match.end(0))