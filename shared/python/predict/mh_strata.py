"""
最後更新：2025 年 11 月 9 日
"""

from phonology import MHSyllable


def 推導梅縣話層次(小韻):
    syl = MHSyllable.parse_pinyin(小韻["推導梅縣話"])

    syl_vern = syl
    # 非組
    if 小韻["組"] == "幫" and syl.initial in list("fv"):
        syl_vern = MHSyllable(
            {"幫": "p", "滂": "pʰ", "並": "pʰ", "明": "m"}[小韻["聲母"]],
            "j" if 小韻["攝"] in "流宕" else syl.medial,
            syl_vern.nucleus,
            syl_vern.coda,
            syl_vern.tone,
        )
    # 匣母合口
    if 小韻["聲母"] == "匣" and 小韻["呼"] == "合":
        syl_vern = MHSyllable("v", *syl_vern.tuple[1:])
    # 梗攝
    if 小韻["攝"] == "梗" and 小韻["呼"] == "開" and 小韻["組"] != "影":
        syl_vern = MHSyllable(
            syl_vern.initial,
            "j"
            if syl_vern.nucleus == "i"
            and not (小韻["等"] == "四" and 小韻["組"] in "端來見")
            else "",
            "a",
            "ŋ" if 小韻["聲調"] != "入" else "k",
            syl_vern.tone,
        )
        # TODO 梗合
    # 咍韻
    if 小韻["韻系"] == "咍" and syl_vern.nucleus == "a":
        syl_vern = MHSyllable(syl_vern.initial, "", "a", "i", syl_vern.tone)
    # 齊韻
    if 小韻["韻系"] == "齊" and 小韻["呼"] == "開":
        syl_vern = MHSyllable(syl_vern.initial, "", "e", "", syl_vern.tone)
    # 上古文部
    if (
        ((小韻["韻系"] == "眞" and 小韻["重紐"] == "B") or 小韻["韻系"] == "欣")
        and 小韻["組"] in "見影"
        and 小韻["呼"] == "開"
    ):
        syl_vern = MHSyllable(
            syl_vern.initial,
            "j",
            "u" if 小韻["聲調"] != "入" else "a",
            syl_vern.coda,
            syl_vern.tone,
        )
    # CHECK 止攝合口 oi
    if (
        小韻["攝"] == "蟹"
        and 小韻["等"] == "一"
        and 小韻["呼"] == "合"
        and (小韻["組"] in "幫端影" or 小韻["聲母"] == "疑")
    ):
        syl_vern = MHSyllable(syl_vern.initial, "", "o", "i", syl_vern.tone)
    # 五 類字
    if 小韻["聲母"] == "疑" and 小韻["韻系"] == "模":  # 三等有 魚女
        syl_vern = MHSyllable("ŋ", "", "", "", syl_vern.tone)
    # 輪 類字
    if (
        小韻["聲母"] == "來"
        and 小韻["攝"] == "臻"
        and 小韻["等"] == "三"
        and 小韻["呼"] == "合"
    ):
        syl_vern = MHSyllable("l", "", "i", syl_vern.coda, syl_vern.tone)
    # MAYBE 上古歌部 ai  溪母 h  濁上歸陰平

    if syl_vern != syl:
        return [["白", syl_vern.pinyin()]]
    return []
