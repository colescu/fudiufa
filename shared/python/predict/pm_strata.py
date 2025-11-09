from phonology import PMSyllable


def 推導普通話層次(小韻):
    syl = PMSyllable.parse_pinyin(小韻["推導普通話"])

    syl_vern = None
    # 入聲韻
    if 小韻["聲調"] == "入":
        if 小韻["攝"] in "江宕":
            syl_vern = PMSyllable(
                syl.initial,
                *{
                    "ɤ": ("", "a", "u"),
                    "o": ("", "a", "u"),
                    "wo": ("", "a", "u"),
                    "ɥe": ("j", "a", "u"),
                }[syl.final],
                syl.tone,
            )
        if 小韻["攝"] in "梗曾" and 小韻["呼"] == "開" and syl.final in ["o", "ɤ"]:
            syl_vern = PMSyllable(
                syl.initial, "", "a" if 小韻["等"] != "一" else "e", "i", syl.tone
            )
        # MAYBE 通三 ou 六肉熟宿軸
    # 行 類字
    if (
        小韻["攝"] == "梗"
        and 小韻["等"] == "二"
        and 小韻["呼"] == "開"
        and 小韻["聲調"] != "入"
        and syl.initial in ["", "k", "kʰ", "h"]
    ):
        syl_vern = PMSyllable(
            {
                "": "",
                "k": "tɕ",
                "kʰ": "tɕʰ",
                "h": "ɕ",
            }[syl.initial],
            "",
            "i",
            "ŋ",
            syl.tone,
        )

    syl_lit = None
    # 類南京型平翹舌
    if syl.initial in ["ʈʂ", "ʈʂʰ", "ʂ"] and (
        (
            小韻["組"] == "莊"
            and (
                (小韻["攝"] == "止" and 小韻["呼"] == "開")
                or 小韻["攝"] in "遇流深"
                or (小韻["攝"] == "曾" and 小韻["呼"] == "開" and 小韻["聲調"] == "入")
            )
        )
        or (
            小韻["組"] in "知莊"
            and 小韻["攝"] == "梗"
            and 小韻["等"] == "二"
            and 小韻["呼"] == "開"
            and 小韻["聲調"] == "入"
        )
    ):
        syl_lit = PMSyllable(
            {
                "ʈʂ": "ts",
                "ʈʂʰ": "tsʰ",
                "ʂ": "s",
            }[syl.initial],
            syl.medial,
            syl.nucleus,
            syl.coda,
            syl.tone,
        )

    return [
        [stratum, syllable.pinyin()]
        for stratum, syllable in [("白", syl_vern), ("文", syl_lit)]
        if syllable is not None
    ]
