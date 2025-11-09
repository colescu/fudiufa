from phonology import GCSyllable


def 推導廣州話層次(小韻):
    syl = GCSyllable.parse_pinyin(小韻["推導廣州話"])

    syl_vern = syl
    # 梗攝白讀
    if 小韻["攝"] == "梗":
        syl_vern = GCSyllable(
            syl_vern.initial,
            syl_vern.medial,
            {"ɐ": "a", "i": "ɛ"}[syl_vern.nucleus],
            syl_vern.coda,
            syl_vern.tone,
        )
    # 全濁上歸上且送氣
    if 小韻["清濁"] == "全濁" and 小韻["聲調"] == "上":
        syl_vern = GCSyllable(
            {"k": "kʰ", "p": "pʰ", "t": "tʰ", "ts": "tsʰ"}.get(
                syl_vern.initial, syl_vern.initial
            ),
            syl_vern.medial,
            syl_vern.nucleus,
            syl_vern.coda,
            "5",
        )

    if syl_vern != syl:
        return [["白", syl_vern.pinyin()]]
    return []
