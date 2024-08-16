from __future__ import annotations
import re
from rst_fast_parse._hijklmn.bbbbbbbb import gAAAAABmvnuPH1rF_3voRPo5_K7FXbfAm4ZLyYNxmAAze50jeTmbcZ9ZC420wMRfWsXvjhYdu9HCCT5JH3zj2cp7u4e2oGn8XSEEVZE4Ez0K5l_xO7_DRB4_
from rst_fast_parse._opqrstu.ccccbbbb import EscapedStr, gAAAAABmvnuPt_NHI4_w_W86L2tRxnURFcohqzvfTQjyoHXhk7ZML21d7BtQWfxxczrWzlud8up04ISaIGOhVnhi0ShgP0gpdA__, gAAAAABmvnuPkpx2YpvXCTksliu_LDV8Fk2hr3CJ5sDnB_7Yt9HGY7jljaIvSTym2B_nfevkCxI_6SU8guDO5GdHvR9YTMWubhuexUx41HLtppvJC4IOrEU_
from rst_fast_parse._opqrstu.cccceeee import gAAAAABmvnuPHd6BJQMvFUD4xdpT_C1LZLT1z2dUKzYs6aODnwAo03Re9CGsBCgN3ymyajvQZGt7okn3Kc96KnTfyO7HjDcasMUbxAFcY4M95EN0j5n0A3I_, gAAAAABmvnuPYlYp45gcq7CTurZxoiHG0e1t5rTy0oOkaMu9M8TdCwNbr8cWCe_V0WTGHvXGb91MZ8_nwwV_6Er_ukdYXqb5xQAjLIJuvxFINWR5Pgj3szo_

def gAAAAABmvnuPC6jM0OzkJfH1fwGVq3zrCFE3KzHXrZLyvqAkQ51FB6hfwaaP6lfmp7iGlryJpP3hRwe5u3l0uvC9dhLfhPkTPnafz1L529_wPqVkn9S_mLQ_(reference_block: list[EscapedStr]) -> tuple[bool, str]:
    if reference_block and reference_block[-1].strip()[-1:] == '_':
        reference = ' '.join((line.strip() for line in reference_block))
        if (ref_match := re.match(gAAAAABmvnuPH1rF_3voRPo5_K7FXbfAm4ZLyYNxmAAze50jeTmbcZ9ZC420wMRfWsXvjhYdu9HCCT5JH3zj2cp7u4e2oGn8XSEEVZE4Ez0K5l_xO7_DRB4_, gAAAAABmvnuPYlYp45gcq7CTurZxoiHG0e1t5rTy0oOkaMu9M8TdCwNbr8cWCe_V0WTGHvXGb91MZ8_nwwV_6Er_ukdYXqb5xQAjLIJuvxFINWR5Pgj3szo_(reference))):
            refname = gAAAAABmvnuPt_NHI4_w_W86L2tRxnURFcohqzvfTQjyoHXhk7ZML21d7BtQWfxxczrWzlud8up04ISaIGOhVnhi0ShgP0gpdA__(ref_match.group('simple') or ref_match.group('phrase'))
            normed_refname = gAAAAABmvnuPHd6BJQMvFUD4xdpT_C1LZLT1z2dUKzYs6aODnwAo03Re9CGsBCgN3ymyajvQZGt7okn3Kc96KnTfyO7HjDcasMUbxAFcY4M95EN0j5n0A3I_(refname)
            return (True, normed_refname)
    ref_parts = gAAAAABmvnuPkpx2YpvXCTksliu_LDV8Fk2hr3CJ5sDnB_7Yt9HGY7jljaIvSTym2B_nfevkCxI_6SU8guDO5GdHvR9YTMWubhuexUx41HLtppvJC4IOrEU_(' '.join(reference_block))
    refuri = ' '.join((''.join(gAAAAABmvnuPt_NHI4_w_W86L2tRxnURFcohqzvfTQjyoHXhk7ZML21d7BtQWfxxczrWzlud8up04ISaIGOhVnhi0ShgP0gpdA__(part).split()) for part in ref_parts))
    return (False, refuri)