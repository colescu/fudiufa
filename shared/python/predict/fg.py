"""
從中古漢語推導撫州話（老文讀）
最後更新：2025 年 11 月 8 日

This file defines a function to derive the expected Fuzhou Gan (FG) reflex
of a Middle Chinese (MC) syllable.
"""

from .predictor import Predictor
from .constants import 非敷奉微_韻系


def 推導聲母(聲母, 介音, 韻腹, 韻系, 攝, 等, 呼):
    是細音 = 介音 == "" and 韻腹 in list("iy") or 介音 in list("jɥ")
    是合口 = 介音 == "w" or 介音 == "" and 韻腹 == "u"
    match 聲母:
        case "幫":
            if 等 == "三" and 韻系 in 非敷奉微_韻系:
                return "f"
            return "p"
        case "滂" | "並":
            if 等 == "三" and 韻系 in 非敷奉微_韻系:
                return "f"
            return "pʰ"
        case "明":
            if 等 == "三" and 韻系 in 非敷奉微_韻系 and 韻系 not in "尤東":
                return "w"  # 白讀 m
            return "m"
        case "端" | "章":
            # 章組端讀
            return "t"
        case "透" | "定" | "昌":
            # 透定白讀 h
            return "tʰ"
        case "知":
            # 知組三等端讀
            match 等:
                case "二":
                    return "ts"
                case "三":
                    return "t"
        case "徹" | "澄":
            match 等:
                case "二":
                    return "tsʰ"
                case "三":
                    return "tʰ"
        case "泥" | "娘":
            # 泥母洪音 n > l
            if 是細音:
                return "n"
            return "l"
        case "來":
            # 來母細音 l > t
            if 是細音:
                return "t"
            return "l"
        case "精" | "莊":
            # 尖團合流 平翹舌合流
            # 莊組不接細音
            if 是細音:
                return "tɕ"
            return "ts"
        case "清" | "從" | "初" | "崇":
            if 是細音:
                return "tɕʰ"
            return "tsʰ"
        case "心" | "邪" | "生" | "俟" | "常" | "書" | "船":  # 俟 無常用字
            if 是細音:
                return "ɕ"
            return "s"
        case "日":
            # CHECK 日母層次混亂
            if (攝 in "止蟹" and 呼 == "合") or (攝 in "效宕咸"):
                # *nɥi > lwi 蕊
                # *njau > leu 擾
                # *njoŋ > loŋ 讓
                # *njɛn > lɛn 染
                # 臻開 *nin > lin? 人
                return "l"
            if (
                (攝 in "止遇曾" and 介音 == "")
                or (攝 in "通流")
                or (攝 == "山" and 呼 == "開")
            ):
                # *ny? > ɛ 如
                # *nin > in 仍
                # *njuŋ > juŋ 絨
                # *nju > ju 柔
                # *njɛn > jɛn 然
                return ""
            if not 是細音:  # *nai > lai 無常用字
                return "l"
            return "n"
        case "見":
            # 尖團合流
            if 是細音:
                return "tɕ"
            return "k"
        case "溪" | "羣":
            if 是細音:
                return "tɕʰ"
            return "kʰ"
        case "疑":
            if 是合口:
                return ""
            if 是細音:
                return "n"
            return "ŋ"
        case "影":
            if 是合口 or 是細音:
                return ""
            return "ŋ"
        case "曉" | "匣":
            # 匣母白讀 w
            if 是合口:
                return "f"
            match 等:
                case "一" | "二":
                    return "h"
                case "三" | "四":
                    return "ɕ"
        case "云" | "以":
            return ""
    raise Exception("聲母 not found!")


def 推導介音(等, 呼, 組, 聲母, 韻系, 攝, 韻腹, 韻尾):
    if 組 == "幫" and 韻系 in 非敷奉微_韻系:
        if 聲母 == "明" and 韻系 == "尤":  # meu
            return ""
        return "w" if 韻腹 != "u" else ""

    默認細音 = "j" if 韻腹 not in list("iɿ") else ""
    默認合口 = "w" if 韻腹 not in list("u") else ""
    默認撮口 = "ɥ" if 韻腹 not in list("yu") else ""
    match 呼:
        case "" | "開":
            match 等:
                case "一" | "二":
                    return ""
                case "三" | "四":
                    if 組 in "知章莊" and 聲母 != "娘":  # 通常丟介音
                        if 組 in "知章" and 攝 == "流":  # tju
                            return 默認細音
                        return ""
                    if 組 == "日" and ((攝 == "止" and 呼 == "開") or 攝 in "遇效宕咸"):
                        return ""  # cf. 聲母
                    return 默認細音
        case "合":
            if 等 in "三四":
                if 聲母 == "日":
                    if 攝 in "止蟹":  # *nɥi > lwi
                        return "w"
                    if 攝 == "臻":  # *nɥun > lun
                        return ""
                    return 默認撮口
                if 攝 in "果山臻" and 組 in "來精見影":
                    # PM üe, üan, ün + 來山 戀 dyon 來臻 輪 dyn
                    return 默認撮口
                if 攝 in "梗曾":  # juŋ, yʔ
                    return "j" if 韻腹 != "y" else ""
            return 默認合口
    raise Exception("介音 not found!")


def 推導韻腹(攝, 韻系, 等, 呼, 組, 聲母, 聲調):
    if 韻系 in "元凡":
        if 組 == "幫":  # an/m
            return "a"
        match 呼:  # 只有 見影
            case "開":  # jɛn
                return "ɛ"
            case "合":  # ɥon
                return "o"

    match 攝:
        case "假":
            return "a"
        case "果" | "江" | "宕":
            return "o"
        case "通":
            return "u"
        case "止":
            if 呼 == "開" and 組 == "日":  # 二 類字
                return "ɛ"
            if 呼 == "開" and 組 in "精莊":
                return "ɿ"
            if 呼 == "合" and 組 == "莊":
                return "ai"  # 爲修正 帥率衰揣
            return "i"
        case "遇":
            match 等:
                case "一":
                    return "u"
                case "三":
                    if 聲母 == "日":  # 如 類字
                        return "ɛ"
                    if 組 in "幫知章莊" and 聲母 != "娘":
                        return "u"
                    return "i"
        case "蟹":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            if 組 == "幫":
                                return "i"
                            if 組 in "見影":  # 鈍音 一等 o ≠ 二等 a
                                return "o"
                            return "a"
                        case "合":
                            return "i"  # 白讀 oi
                case "二":
                    return "a"
                case "三" | "四":
                    return "i"
        case "效":
            if 等 == "三" and (組 in "知章" or 聲母 == "日"):
                return "ɛ"
            return "a"
        case "流":
            match 等:
                case "一":
                    return "ɛ"
                case "三":
                    if 聲母 == "明" and 韻系 == "尤":  # 爲修正 謀牟矛
                        return "ɛ"
                    if 組 == "莊":
                        return "ɛ"
                    return "u"
            match 等:
                case "一" | "二":
                    if 等 == "一" and 呼 == "開" and 組 in "見影":
                        return "o"
                    return "a"
        case "咸" | "山":
            match 等:
                case "一" | "二":
                    if 等 == "一" and (
                        (呼 == "開" and 組 in "見影")  # 鈍音 一等 o ≠ 二等 a
                        or 呼 == "合"
                        # 幫組基本只有 山一開 山二合
                    ):
                        return "o"
                    return "a"
                case "三" | "四":
                    match 呼:
                        case "開":  # jɛn/m
                            return "ɛ"
                        case "合":  # ɥon
                            return "o"
        case "深":
            if 組 == "莊":
                return "ɛ"  # 或非本音
            return "i"
        case "臻":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            return "ɛ"
                        case "合":
                            return "u"
                case "三":
                    match 呼:
                        case "開":
                            if 組 == "莊":
                                return "ɛ"
                            return "i"
                        case "合":
                            if 組 in "幫知章莊日":
                                return "u"
                            return "y"
        case "梗" | "曾":
            # 梗攝白讀 a
            match 等:
                case "一" | "二":
                    return "ɛ"
                case "三" | "四":
                    match 呼:
                        case "開":
                            if 組 == "莊":
                                return "ɛ"
                            return "i"
                        case "合":
                            if 聲調 == "入":  # 爲修正 疫域
                                return "y"
                            return "u"
    raise Exception("韻腹 not found!")


def 推導韻尾(攝, 聲調, 韻腹):
    match 攝:
        case val if val in "止遇果假":
            return ""
        case "蟹":
            return "i" if 韻腹 != "i" else ""  # 例外：話佳娃挂卦
        case val if val in "效流":
            return "u" if 韻腹 != "u" else ""
        case val if val in "深咸臻山":
            return "t" if 聲調 == "入" else "n"
        case val if val in "通江宕":
            return "ʔ" if 聲調 == "入" else "ŋ"
        case val if val in "梗曾":
            if 聲調 == "入":
                return "ʔ"
            else:
                if 韻腹 in list("ɛi"):
                    return "n"  # 白讀 aŋ
                return "ŋ"
    raise Exception("韻尾 not found!")


def 推導聲調(聲調, 清濁):
    match 聲調:
        case "平":
            match 清濁[-1]:
                case "清":
                    return "1"
                case "濁":
                    return "2"
        case "上":
            match 清濁:
                case "全濁":
                    return "6"  # 無視歸入陰平的層次
                case _:
                    return "3"
        case "去":
            match 清濁[-1]:
                case "清":
                    return "5"
                case "濁":
                    return "6"
        case "入":
            match 清濁:
                case "全清" | "次清":
                    return "7"
                case "全濁":
                    return "8"
                case "次濁":
                    return "7"  # 白讀陽入
    raise Exception("聲調 not found!")


def normalize(小韻):
    if 小韻["聲母"] == "w":
        小韻["聲母"] = ""
        小韻["介音"] = "w" if 小韻["韻腹"] != "u" else ""
    if 小韻["韻腹"] == "ai":  # wai
        小韻["韻腹"], 小韻["韻尾"] = "a", "i"

    # phonological constraints
    if 小韻["介音"] == "w" and not (
        小韻["聲母"] in ["k", "kʰ", ""]
        or (
            小韻["聲母"] in ["t", "tʰ", "n", "l", "ts", "tsʰ", "s"]
            and 小韻["韻腹"] == "i"
            and 小韻["韻尾"] == ""
        )
    ):  # delete -w-
        小韻["介音"] = ""


推導撫州話 = Predictor(module=globals(), name="撫州話").predict
