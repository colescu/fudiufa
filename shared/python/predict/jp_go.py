"""
最後更新：2025 年 11 月 9 日（草稿版）
"""

from .predictor import Predictor
from phonology import JPSyllable


def 推導聲母(聲母, 介音, 韻):
    韻母 = 介音 + 韻
    match 聲母:
        case "幫" | "滂":
            return "h"
        case "並":
            return "b"
        case "明":
            return "m"
        case "端" | "透" | "知" | "徹":
            return "t"
        case "定" | "澄":
            return "d"
        case "泥" | "娘" | "日":
            return "n"
        case "來":
            return "r"
        case val if val in "精清心莊初生章昌書":
            return "s"
        case val if val in "從邪崇俟常船":
            return "z"
        case "見" | "溪" | "曉":
            return "k"
        case "羣" | "疑" | "匣":
            if 聲母 == "匣" and 韻母.startswith(("wa", "we")) and 韻[-1] != "n":
                return ""  # 部分 g
            return "g"
        case "影" | "云" | "以":
            return ""
    raise Exception("聲母 not found!")


def 推導介音(等, 呼, 組, 聲母, 韻系, 攝, 重紐, 韻):  # 例外多
    # 除此以外不推導細音
    if 聲母 == "以":
        return "y" if not 韻.startswith(("i", "e")) else ""

    默認合口 = (
        "w"
        if not 韻.startswith(("u", "y"))
        and (
            組 in "見影" or (組 != "幫" and 聲母 != "娘" and 韻 == "i")  # 止攝
        )
        else ""
    )
    match 呼:
        case "" | "開":
            if 韻系 == "東" and 等 == "三" and 聲母 == "影":  # 爲修正 郁彧
                return "w"
            return ""
        case "合":
            if 等 in "三四":
                if 重紐 == "A":
                    return ""
                if 攝 == "梗" and 等 == "三":
                    return ""  # 例外多
            return 默認合口
    raise Exception("介音 not found!")


def 推導韻(攝, 韻系, 等, 呼, 重紐, 組, 聲母, 聲調):
    is_checked_tone = 聲調 == "入"
    match 攝:
        case "假":
            if 組 in "幫見影" and 聲母 != "以":
                return "e"
            if 組 in "知" and 呼 == "合" or 聲母 == "娘":  # 常用字僅有 拏
                return "a"
            return "ya"
        case "果":
            if 等 == "三":
                if 組 == "影":  # 爲修正 靴
                    return "e"
                return "ya"
            return "a"
        case "止":
            if 韻系 == "之" and (組 == "見" or 聲母 == "曉"):  # 即見影但非零聲母
                return "o"
            if 韻系 == "微" and 呼 == "開" and 組 in "見影":  # 合口也很多 we
                return "e"
            if 聲母 == "以" and 呼 == "合":  # 爲修正 惟維
                return "yui"
            return "i"
        case "遇":  # 複雜 (y)u/o
            match 韻系:
                case "模":
                    if 聲母 == "明":
                        return "o"
                    return "u"  # 例外多 尤其是定從疑匣
                case "虞":
                    if 組 in "知日":
                        return "yuu"  # 例外：廚 du
                    if 組 == "莊":
                        return "yu"
                    return "u"  # 常母例外多
                case "魚":
                    if 組 in "知章莊日" or 聲母 in "邪":  # 邪母?
                        return "yo"  # 例外：初 so
                    return "o"
        case "蟹":
            match 組:
                case val if val in "端來知精":
                    return "ai"
                case val if val in "莊章":
                    return "e"
                case "日":  # 無常用字
                    return "ei"
                case "幫":  # 例外多 ai
                    if 等 in "一四":
                        if 韻系 == "灰":
                            return "e"
                        return "ai"
                    if 韻系 == "廢":
                        return "o"
                    return "e"
                case "見" | "影":
                    if 等 == "一" and 呼 == "開" or 韻系 == "祭" and 重紐 == "B":
                        return "ai"  # 咍韻部分 ke / o
                    return "e"
        case "效":
            match 等:
                case "一":
                    if 組 == "幫" and 等 == "一":
                        return "ou"  # 幫母多 o
                    return "au"
                case "二" | "三" | "四":
                    return "eu"
        case "流":
            match 韻系:
                case "侯":
                    return "u"  # 明母多 o
                case "尤":
                    if 組 in "知日":
                        return "iu"
                    if 組 in "精莊章":
                        return "yu"  # 例外：修 su 章組部分 u
                    return "u"
                case "幽":
                    return "iu"
        case "咸":
            match 等:
                case "一":
                    match 韻系:
                        case "覃":
                            return "om"  # 例外：南男 namu 婪纜 ramu 納 nahu
                        case "談":
                            return "am"
                case "二" | "三" | "四":
                    if 韻系 in "凡嚴":
                        return "om"
                    return "em"
        case "深":
            if 組 in "幫見影" and 聲母 != "以":
                return "om"  # 例外：稟 himu 揖 ihu
            return "im"
        case "山":
            match 等:
                case "一":
                    return "an"
                case "二" | "三" | "四":
                    return "en"  # 例外：八 hati
        case "臻":
            match 等:
                case "一":
                    return "on"
                case "三":
                    if 韻系 == "元":
                        return "on"
                    if 韻系 == "文":
                        if 聲母 == "明" or 聲母 in "幫滂" and is_checked_tone:
                            return "on"
                        return "un"
                    if 組 in "精莊知章" and 呼 == "合":
                        return "yun"
                    if 組 in "見影" and (重紐 == "B" or 韻系 == "欣"):
                        return "on"
                    return "in"
        case "江" | "宕":
            if 攝 == "江" and (組 == "幫" and 聲母 != "明" or not is_checked_tone):
                return "oŋ"  # 江攝其他也有部分 oku
            if 等 == "三" and 組 in "知章莊日":
                return "yaŋ"
            return "aŋ"
        case "通":
            if not is_checked_tone:  # CHECK 複雜 u(u)
                match 韻系 + 等:
                    case "東一":
                        if 組 == "端":
                            return "uu"
                        return "u"
                    case "冬一":
                        if 組 == "端":
                            return "ou"
                        return "o"  # 字少
                    case "東三":
                        if 組 in "知日":
                            return "yuu"
                        if 組 in "幫精莊見":
                            return "uu"
                        if 組 == "章":
                            return "yu"
                        return "u"
                    case "鍾三":
                        if 組 in "知日" or 聲母 == "以":
                            return "yuu"
                        if 組 in "幫見":  # 不接莊組
                            return "uu"
                        if 組 in "精章" or 聲母 == "影":
                            return "yu"
                        return "u"
            else:
                if 等 == "三" and 韻系 == "東" and 聲母 not in "明來":
                    if 組 in "知日見影":
                        return "iku"
                    if 組 == "章":
                        return "yuku"
                    return "uku"
                return "oku"
        case "梗":
            if 呼 == "合" and 等 == "二":
                return "aŋ"
            return "yaŋ"
        case "曾":
            if (
                聲母 == "匣" and 等 == "一" and 呼 == "合" and is_checked_tone
            ):  # 爲修正 或惑
                return "aku"
            if 等 == "三":
                if 組 in "精見影" and 聲母 not in "云以":
                    return "oŋ"
                return "you" if not is_checked_tone else "iki"
            return "oŋ"
    raise Exception("韻 not found!")


def normalize(小韻):
    if 小韻["韻"][-1] in "mnŋ":  # 韻尾
        小韻["韻"] = (
            小韻["韻"][:-1]
            + {
                "m": ["mu", "hu"],
                "n": ["n", "ti"],
                "ŋ": ["u", "ku"] if 小韻["韻"][-2] not in "ie" else ["i", "ki"],
            }[小韻["韻"][-1]][int(小韻["聲調"] == "入")]
        )

    if 小韻["韻"].startswith(("y", "w")):  # incorporated 介音
        小韻["介音"], 小韻["韻"] = 小韻["韻"][0], 小韻["韻"][1:]
    if (
        小韻["聲母"] not in ["k", "g", ""] and 小韻["介音"] == "w" and 小韻["韻"] == "i"
    ):  # kwi vs tui
        小韻["介音"], 小韻["韻"] = "", "ui"

    # phonological constraints
    if 小韻["聲母"] != "" and 小韻["介音"] == "w" and 小韻["韻"].startswith("o"):
        小韻["介音"] = ""


推導日本語吳音 = Predictor(
    module=globals(), name="日本語吳音", parts=["韻", "介音", "聲母"]
).predict


def 推導日本語層次(小韻):
    go = JPSyllable.parse_pinyin(推導日本語吳音(小韻)).pinyin(show_small_kana=False)
    if go != 小韻["推導日本語"]:
        return [["吳", go]]
    return []
