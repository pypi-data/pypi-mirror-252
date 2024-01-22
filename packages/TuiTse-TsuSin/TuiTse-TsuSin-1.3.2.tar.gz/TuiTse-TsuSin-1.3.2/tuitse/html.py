from django.utils.html import format_html
from tuitse import THAU_JI, LIAN_JI, KHIN_SIANN_JI
from kesi.butkian.kongiong import 敢是拼音字元


def tuitse_html(kiamtsa_tinliat):
    html = ''
    tshamsoo = []
    su_html = ''
    su_tshamsoo = []
    ting_tsit_hanlo_kam_si_lomaji = False
    ting_tsit_lomaji_kam_si_lomaji = False
    for ji in kiamtsa_tinliat:
        # Kuat-tīng Tsit jī ê hîng ài liân-jī-hû--bô
        hanlo_kam_si_lomaji = 敢是拼音字元(ji[0][-1:])

        if hanlo_kam_si_lomaji and ting_tsit_hanlo_kam_si_lomaji:
            hanlo_kam_ai_lian = True
        else:
            hanlo_kam_ai_lian = False

        ting_tsit_hanlo_kam_si_lomaji = hanlo_kam_si_lomaji

        # Kuat-tīng Tsit jī ê im ài liân-jī-hû--bô
        lomaji_kam_si_lomaji = 敢是拼音字元(ji[1][-1:])

        if lomaji_kam_si_lomaji and ting_tsit_lomaji_kam_si_lomaji:
            lomaji_kam_ai_lian = True
        else:
            lomaji_kam_ai_lian = False

        ting_tsit_lomaji_kam_si_lomaji = lomaji_kam_si_lomaji

        if ji[2] == THAU_JI:
            # Thòo sû ê html
            if su_html:
                html += "<ruby>{}</ruby>".format(su_html)
                tshamsoo += su_tshamsoo
            # Html tîng-lâi
            su_html, su_tshamsoo = _sng_ji_html(ji)
            continue

        if ji[2] == LIAN_JI:
            tiauhu = '-'
        elif ji[2] == KHIN_SIANN_JI:
            tiauhu = '--'
        else:
            raise RuntimeError('一定愛設定頭字、連字、a̍h-sī輕聲')

        if lomaji_kam_ai_lian:
            su_html += "<rb>{}</rb>"
            su_tshamsoo.append(tiauhu)
        else:
            su_html += "<rb>&nbsp;</rb>"

        if hanlo_kam_ai_lian:
            su_html += "<rt>{}</rt>"
            su_tshamsoo.append(tiauhu)
        else:
            su_html += "<rt></rt>"

        sng_html, sng_tshamsoo = _sng_ji_html(ji)
        su_html += sng_html
        su_tshamsoo += sng_tshamsoo
    # Thòo bué sû ê html
    html += "<ruby>{}</ruby>".format(su_html)
    tshamsoo += su_tshamsoo
    return format_html(html, *tshamsoo)


def _sng_ji_html(ji):
    if ji[3]:
        return "<rb>{}</rb><rt>{}</rt>", [ji[1], ji[0]]
    if ji[1]:
        return "<rb class='fail'>{}</rb><rt class='fail'>{}</rt>", [
            ji[1], ji[0]
        ]
    return "<rb class='fail'>&nbsp;&nbsp;</rb><rt class='fail'>{}</rt>", [
        ji[0]
    ]
