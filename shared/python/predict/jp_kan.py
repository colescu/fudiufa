"""
最後更新：2025 年 11 月 9 日

output format: NR, show_long_vowel=False
"""

from .predictor import Predictor


def 推導聲母(聲母, 攝, 聲調):
    is_checked_tone = 聲調 == "入"
    match 聲母:
        case "幫" | "滂" | "並":
            return "h"
        case "明":
            if 攝 == "梗" and not is_checked_tone:
                return "m"
            return "b"
        case "端" | "透" | "定" | "知" | "徹" | "澄":
            return "t"
        case "泥" | "娘":
            if 攝 == "梗" and not is_checked_tone:
                return "n"
            return "d"
        case "來":
            return "r"
        case val if val in "精清從心邪莊初崇生俟章昌常書船":
            return "s"
        case "日":
            return "z"
        case "見" | "溪" | "羣" | "曉" | "匣":
            return "k"
        case "疑":
            return "g"
        case "影" | "云" | "以":
            return ""
    raise Exception("聲母 not found!")


def 推導介音(等, 呼, 組, 聲母, 韻系, 攝, 重紐, 韻):  # 例外多
    默認細音 = "y" if not 韻.startswith(("i", "e")) else ""
    默認合口 = (
        "w"
        if not 韻.startswith("u")
        and (
            組 in "見影" or (組 != "幫" and 聲母 != "娘" and 韻 == "i")  # 止攝
        )
        else ""
    )
    match 呼:
        case "" | "開":
            match 等:
                case "一" | "二":
                    if 聲母 == "影" and 韻系 in "模東":  # 烏 wo 翁 wou
                        return "w"
                    return ""
                case "三" | "四":
                    if 組 == "幫" and 攝 != "曾":
                        return ""
                    if 組 == "莊" and 攝 != "通":  # 遇攝多 y
                        return ""
                    if 韻系 == "魚" and 組 == "莊" or 韻系 == "虞":
                        return ""
                    if 韻系 == "東" and 聲母 == "影":  # 爲修正 郁彧
                        return "w"
                    if 韻系 == "廢":  # 爲修正 乂刈
                        return ""
                    return 默認細音
        case "合":
            if 等 in "三四":
                if 重紐 == "A":
                    return ""
                if 聲母 == "以" and 攝 != "止":
                    return ""
                if 攝 == "果" and 組 == "見":  # 爲修正 茄瘸
                    return "y"
                if 攝 == "宕" and 聲母 in "見溪羣疑曉匣":  # 今聲母 k
                    return "wy"
                if 攝 == "梗" and 等 == "三":
                    return ""  # 例外多 w
                if 攝 == "曾":  # 爲修正 洫域
                    return "wy"
            return 默認合口
    raise Exception("介音 not found!")


def 推導韻(攝, 韻系, 等, 呼, 組, 聲母, 聲調):
    is_checked_tone = 聲調 == "入"
    match 攝:
        case "假" | "果":
            return "a"
        case "止":
            return "i"
        case "遇":  # 複雜
            if 韻系 == "虞":  # incorporate 介音
                if 組 == "知":
                    return "yuu"
                if 組 in "精章日" or 聲母 == "以":
                    return "yu"
                return "u"
            return "o"
        case "蟹":
            match 等:
                case "一" | "二":
                    return "ai"
                case "三" | "四":
                    if 韻系 == "廢":
                        return "ai"
                    return "ei"
        case "效":
            match 等:
                case "一" | "二":
                    if 組 == "幫" and 等 == "一":
                        return "ou"
                    return "au"
                case "三" | "四":
                    return "eu"
        case "流":
            match 等:
                case "一":
                    return "ou"
                case "三":
                    if 組 in "幫莊" and 韻系 == "尤":
                        if 聲母 in "明生":  # 矛謀眸 搜瘦
                            return "ou"
                        return "uu"
                    return "iu"  # ≠ yu
        case "咸":
            match 等:
                case "一" | "二":
                    return "am"
                case "三" | "四":
                    if 韻系 == "凡":
                        return "am"
                    return "em"
        case "深":
            if 組 == "莊" and is_checked_tone:
                return "ohu"
            return "im"
        case "山":
            match 等:
                case "一" | "二":
                    return "an"
                case "三" | "四":
                    return "en"
        case "臻":
            match 等:
                case "一":
                    return "on"
                case "三":
                    if 韻系 == "元":
                        if 組 == "幫":
                            return "an"
                        return "en"
                    if 韻系 == "文":
                        return "un"
                    if 組 in "精知章日" and 呼 == "合":
                        return "yun"
                    return "in"
        case "江" | "宕":
            return "aŋ"
        case "通":
            if 等 == "三" and 韻系 == "東":
                if not is_checked_tone:
                    if 組 != "幫":
                        return "uu"
                else:
                    if 聲母 == "明":
                        return "oku"
                    if 組 in "來知日見影":
                        return "iku"
                    return "uku"
            return "oŋ"
        case "梗":  # TODO
            match 等:
                case "二":
                    if 聲母 in "來生" and not is_checked_tone:  # 冷 生…
                        return "ei"
                    return "aŋ"
                case "三" | "四":
                    return "eŋ"
        case "曾":
            return "oŋ"
    raise Exception("韻 not found!")


def normalize(小韻):
    if 小韻["韻"][-1] in "mnŋ":  # 韻尾
        小韻["韻"] = (
            小韻["韻"][:-1]
            + {
                "m": ["mu", "hu"],
                "n": ["n", "tu"],
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
    if 小韻["聲母"] == "" and 小韻["介音"] == "wy":
        小韻["介音"] = "y"
    if 小韻["聲母"] != "" and 小韻["介音"] == "w" and 小韻["韻"].startswith("o"):
        小韻["介音"] = ""


推導日本語漢音 = Predictor(
    module=globals(), name="日本語漢音", parts=["韻", "介音", "聲母"]
).predict
