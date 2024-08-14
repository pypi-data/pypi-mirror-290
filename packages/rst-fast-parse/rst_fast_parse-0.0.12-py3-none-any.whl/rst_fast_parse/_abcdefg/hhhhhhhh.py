from __future__ import annotations
import re
from typing import Callable, Literal
from typing_extensions import TypeAlias
from rst_fast_parse.core import gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_, gAAAAABmuydMiLdU_dp59oVEPGBNv68vj5wG7_22Bvg5bZ03OT2G_QCzmRWERmHgVHtQYXo1mUcSENx4LswwbgB9jit4vTIw9A__, gAAAAABmuydMZvEEZ_3jzwR8q9BsCcTFE50XNDCYTKN1JJpJvt4d7iPcmxP85UNh63Bidy8VWJ_6TQqrL0uFnzCWChXUvr1w_sY_V65KaX_WzQiRcnhAjbk_, gAAAAABmuydMRweAvNUw6_RAhvNTsyROtSlhzkieQGDs7aJ4PmDgfnBl2w5qXfrC0rD9MRHqzLLKUy6bmJaLqiC8ueZoeMhy1g__
from rst_fast_parse.elements import ListElement, ListItemElement
from rst_fast_parse._hijklmn.pppppppp import gAAAAABmuydMQphPs_6pFZI7_Lwnag2VS6KCsuIBZ4QY5F_IIomrhRpJKEekbjYR4CbJZ7g_NLVnvpFurt_l5xABrGjuxgTPRw__
from rst_fast_parse.source import gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__
from rst_fast_parse._opqrstu.tttttttt import gAAAAABmuydMtpIKrLY1a_pKduI6MueCkbIYGfpBRsBZiRWXongXyhPOvqKhvPJzED8BoZI18gBT9JeShqm9wsx8OHoZDYramttYMF63EzbtwZZh_M9vhbU_
from rst_fast_parse._opqrstu.uuuuuuuu import gAAAAABmuydMDKn8AiAPEus6utiXPVbHyEXVdp2Zjo3NLRdr7KzDnbxXYhywOUCC29nvxg4YbR6rGSn_4QH4K6UvcsHPfFSt_w__

def gAAAAABmuydMsjihxBLjS0g_mxLtLpHidYZWF5WqcVNd58NgcaDMutXOl1D6xBg8w_XBnMdDszy8ygYDx6x_48ZUelZ9Neb3fpYnCLxhoa__CpjYrOsqI_o_(source: gAAAAABmuydMVJgMnmSTyLrkYdxKPQdHOKbYiMjkRU_PfqS4fOZ24_zmOB0oCtkvC_ztGe1VFoNh5MyXYh8V_BBPR27wINYhDg__, parent: gAAAAABmuydMRweAvNUw6_RAhvNTsyROtSlhzkieQGDs7aJ4PmDgfnBl2w5qXfrC0rD9MRHqzLLKUy6bmJaLqiC8ueZoeMhy1g__, diagnostics: gAAAAABmuydMZvEEZ_3jzwR8q9BsCcTFE50XNDCYTKN1JJpJvt4d7iPcmxP85UNh63Bidy8VWJ_6TQqrL0uFnzCWChXUvr1w_sY_V65KaX_WzQiRcnhAjbk_, context: gAAAAABmuydMiLdU_dp59oVEPGBNv68vj5wG7_22Bvg5bZ03OT2G_QCzmRWERmHgVHtQYXo1mUcSENx4LswwbgB9jit4vTIw9A__, /) -> gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_:
    if (init_line := source.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__) is None:
        return gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMNoVXrdqJvzMnoVrlYn_r3Ve1p2VbhCA8q06J5yPCK6aa322xvsPFlWI_vQyJJvvsEyWZHSCuNOqhrJs9iswRJw__
    if (result := gAAAAABmuydM_Zs3kWeS2hypO3NL3EtRPV0zZtVmMjXUYCDOnI7SMOqLKwGAopWeS6GCLxagIDfLVVArosACGFjZAB_OVst8P8Q43zjdkObxSkTftSRJxQQ_(init_line.content)) is None:
        return gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMKf1XPP798dMRx3PTLCDxb3oSW_v3i3TShC0b1ZBMlwGJvJcJxBiYfbIhB_70sjOifWGPv47p0bdjpiKqfq8JRA__
    init_format, init_type, init_ordinal, _ = result
    last_auto = init_type == 'auto'
    last_ordinal: int | None = None
    if init_type == 'auto':
        init_type = 'arabic'
    if (next_line := source.gAAAAABmuydMjbS8YuuKhsP69b_LVvC78esxs5XU17tNBvFT5M78twv9zAr2BCdXDlxxlpryRxHeuS9otaesRd8zMuXC_yzrRg__()) and (not next_line.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__) and next_line.content[:1].strip() and (not gAAAAABmuydM_Zs3kWeS2hypO3NL3EtRPV0zZtVmMjXUYCDOnI7SMOqLKwGAopWeS6GCLxagIDfLVVArosACGFjZAB_OVst8P8Q43zjdkObxSkTftSRJxQQ_(next_line.content)):
        return gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydMKf1XPP798dMRx3PTLCDxb3oSW_v3i3TShC0b1ZBMlwGJvJcJxBiYfbIhB_70sjOifWGPv47p0bdjpiKqfq8JRA__
    items: list[ListItemElement] = []
    while (gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__ := source.gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__):
        if gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.gAAAAABmuydMLY3WjIO6PlM5TJMKh5cp2xHJZ8tGj9VdturoMbyEGZMJAjf88by_LCd3Uc0Zey3kyo4hBhWIoY_1QiOaoCkMhw__:
            source.gAAAAABmuydMPNXekMCrPsz_vYOvYDs9_oPrgnfp3HgByoOHnDM0959v7DsbYZ6_m4qeg67gi4pyB8POEdOStAS6ZKU5A8yuhQ__()
            continue
        if (result := gAAAAABmuydM_Zs3kWeS2hypO3NL3EtRPV0zZtVmMjXUYCDOnI7SMOqLKwGAopWeS6GCLxagIDfLVVArosACGFjZAB_OVst8P8Q43zjdkObxSkTftSRJxQQ_(gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.content, init_type)) is not None:
            eformat, etype, next_ordinal, char_offset = result
            if eformat != init_format or (etype != 'auto' and (etype != init_type or last_auto or (last_ordinal is not None and next_ordinal != last_ordinal + 1))):
                source.gAAAAABmuydMgGp1zxtMB3LqMXtilFCkg9VkTI4wy3_bYLi0JBOEylSKJahQoLf6NZZxDp0hhstN65CoqNG1cXLcS5Y3vvQntg__()
                break
            if len(gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.content) > char_offset:
                content = source.gAAAAABmuydMPb4zkoCha1wtvezhuTDuxHI2YICB74Hxj5Jlmvh7ZnaoG1W5zx1zk2cZ6NUVogPUDJzx4RwHWMMlD1ChT0MtPMjaO2yl0B1NHRbzkvKzG6A_(char_offset, always_first=True, advance=True)
            else:
                content = source.gAAAAABmuydMYWGOiYMRJte2AIZmsTpE5T8M9dIG1126Umz8TRob4u_BOar5DbSoFetNDDhxxWklCW_tXtv5uahJjW5xiumYvoH9Ov5G2wj8XFPVuaa51dk_(first_indent=char_offset, advance=True)
            list_item = ListItemElement((gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.line, gAAAAABmuydMWORmKn5jshVdawl0HXIIyAiSOnnJ4Ye5DISO6vjqv641ervwhm7rY79I_nPWObfGoHnHKGRsoyiMlWwMmaEmJA__.line if content.gAAAAABmuydMMDFHabcSdIh9mauc3_cVL_vPmICOToRMyXe24NJkI8PyaMKTQge2_LiSPcI2oRpWHdyIgMadE8ZUyD8xCSnCKQ__ is None else content.gAAAAABmuydMMDFHabcSdIh9mauc3_cVL_vPmICOToRMyXe24NJkI8PyaMKTQge2_LiSPcI2oRpWHdyIgMadE8ZUyD8xCSnCKQ__.line))
            items.append(list_item)
            context.gAAAAABmuydMMF7ZY53udCcS2ALzNb0Tz_DMP3IixR1JcbpUdl3ynb7luBKHkl8sLLd7on9MRLssGnahjwAivbf9MRBXSFHPbg__(content, list_item, diagnostics)
            last_auto = etype == 'auto'
            last_ordinal = next_ordinal
            source.gAAAAABmuydMPNXekMCrPsz_vYOvYDs9_oPrgnfp3HgByoOHnDM0959v7DsbYZ6_m4qeg67gi4pyB8POEdOStAS6ZKU5A8yuhQ__()
        else:
            source.gAAAAABmuydMgGp1zxtMB3LqMXtilFCkg9VkTI4wy3_bYLi0JBOEylSKJahQoLf6NZZxDp0hhstN65CoqNG1cXLcS5Y3vvQntg__()
            break
    if items:
        parent.append(ListElement('enum_list', items))
        gAAAAABmuydMtpIKrLY1a_pKduI6MueCkbIYGfpBRsBZiRWXongXyhPOvqKhvPJzED8BoZI18gBT9JeShqm9wsx8OHoZDYramttYMF63EzbtwZZh_M9vhbU_(diagnostics, source, 'Enumerated list')
    return gAAAAABmuydMQpIcseTp2a_x6vkRdemQi7BjIjLK54WK1Euw2x2tfrfcFC7KFRL7hwgsVYK0hMaWeW2NVkRVAoQcY5g5bUdvdHEmjIYcUhrtREWBxAS7Acw_.gAAAAABmuydM_3nhN_OjUBfPISsOcE6uNx7vcMNK1buxeJMBIyldcdVwhb7nmW0jrIJL4sgbZgUGzuOO7yr8rsz0gqVTH3yLwg__
_ParenType: TypeAlias = Literal['parens', 'rparen', 'period']
_EnumType: TypeAlias = Literal['auto', 'arabic', 'loweralpha', 'upperalpha', 'lowerroman', 'upperroman']
gAAAAABmuydMQA2BYeMxdq8z2cgJSwG3Up7x2t6eL_TqocxUfqZ_OWFoz20ehp6oLS6MGfLfBv0GOZRtsN8sS_uIPzCEc_M_4A_l5l7lARU5Jw4MucxUZxg_: dict[_EnumType, tuple[str, _EnumType]] = {'auto': ('^[0-9]+$', 'arabic'), 'arabic': ('^[0-9]+$', 'arabic'), 'loweralpha': ('^[a-z]$', 'loweralpha'), 'upperalpha': ('^[A-Z]$', 'upperalpha'), 'lowerroman': ('^[ivxlcdm]+$', 'lowerroman'), 'upperroman': ('^[IVXLCDM]+$', 'upperroman')}
gAAAAABmuydMcyHz1DsLNzCLLYWjnZHEiF4wWStARDK_qFPghqi4qGmEdd1L9bmSvU7p4UmWPrw25Kop5H4idWXrvupc4aQRfA__: tuple[tuple[str, _EnumType], ...] = (('^[0-9]+$', 'arabic'), ('^[a-z]$', 'loweralpha'), ('^[A-Z]$', 'upperalpha'), ('^[ivxlcdm]+$', 'lowerroman'), ('^[IVXLCDM]+$', 'upperroman'))
gAAAAABmuydMnyxewzFvC53_NlPfLRKDllhdMlRXLOc1piD07q6YfknenvHIRm3o36VGrZlgoJyjUFoa1r_N5jNPt19TgtOzDbN2RzMhwyHsG4piTdFNanA_: dict[_EnumType, Callable[[str], int | None]] = {'auto': lambda t: 1, 'arabic': int, 'loweralpha': lambda t: ord(t) - ord('a') + 1, 'upperalpha': lambda t: ord(t) - ord('A') + 1, 'lowerroman': lambda t: gAAAAABmuydMDKn8AiAPEus6utiXPVbHyEXVdp2Zjo3NLRdr7KzDnbxXYhywOUCC29nvxg4YbR6rGSn_4QH4K6UvcsHPfFSt_w__(t.upper()), 'upperroman': lambda t: gAAAAABmuydMDKn8AiAPEus6utiXPVbHyEXVdp2Zjo3NLRdr7KzDnbxXYhywOUCC29nvxg4YbR6rGSn_4QH4K6UvcsHPfFSt_w__(t)}

def gAAAAABmuydM_Zs3kWeS2hypO3NL3EtRPV0zZtVmMjXUYCDOnI7SMOqLKwGAopWeS6GCLxagIDfLVVArosACGFjZAB_OVst8P8Q43zjdkObxSkTftSRJxQQ_(line: str, expected: None | _EnumType=None) -> None | tuple[_ParenType, _EnumType, int, int]:
    if not (match := re.match(gAAAAABmuydMQphPs_6pFZI7_Lwnag2VS6KCsuIBZ4QY5F_IIomrhRpJKEekbjYR4CbJZ7g_NLVnvpFurt_l5xABrGjuxgTPRw__, line)):
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
        regex, result = gAAAAABmuydMQA2BYeMxdq8z2cgJSwG3Up7x2t6eL_TqocxUfqZ_OWFoz20ehp6oLS6MGfLfBv0GOZRtsN8sS_uIPzCEc_M_4A_l5l7lARU5Jw4MucxUZxg_[expected]
        if re.match(regex, text):
            sequence = result
    elif text == 'i':
        sequence = 'lowerroman'
    elif text == 'I':
        sequence = 'upperroman'
    if sequence is None:
        for regex, result in gAAAAABmuydMcyHz1DsLNzCLLYWjnZHEiF4wWStARDK_qFPghqi4qGmEdd1L9bmSvU7p4UmWPrw25Kop5H4idWXrvupc4aQRfA__:
            if re.match(regex, text):
                sequence = result
                break
        else:
            raise RuntimeError(f'enumerator sequence not matched: {text!r}')
    if (ordinal := gAAAAABmuydMnyxewzFvC53_NlPfLRKDllhdMlRXLOc1piD07q6YfknenvHIRm3o36VGrZlgoJyjUFoa1r_N5jNPt19TgtOzDbN2RzMhwyHsG4piTdFNanA_[sequence](text)) is None:
        return None
    return (fmt, sequence, ordinal, match.end(0))