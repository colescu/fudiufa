"""
從中古漢語推導撫州話（老文讀）
最後更新：2025 年 9 月 27 日

This file defines a function to derive the expected Fuzhou Gan (FG) reflex
of a Middle Chinese (MC) syllable.
"""

import inspect

from .constants import 非敷奉微_韻系


def 推導聲母(
    聲母: str, 介音: str, 韻腹: str, 韻系: str, 攝: str, 等: str, 呼: str
) -> str:
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
                # ? > ɛ 如
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
            match 等:
                case "一" | "二":
                    if 是合口:
                        return "f"
                    return "h"
                case "三" | "四":
                    if 呼 == "合" and 韻腹 == "i" and 攝 not in "梗曾":
                        return "f"
                    if 攝 == "宕" and 呼 == "合":  # 爲修正 況戄
                        return "f"
                    return "ɕ"
        case "云" | "以":
            return ""
    raise Exception("聲母 not found!")


def 推導介音(
    等: str, 呼: str, 組: str, 聲母: str, 韻系: str, 攝: str, 韻腹: str, 韻尾: str
) -> str:
    韻 = 韻腹 + 韻尾
    match 呼:
        case "" | "開":
            三四等默認 = "j" if 韻腹 not in list("iɿ") else ""
            match 等:
                case "一" | "二":
                    return ""
                case "三":
                    if 組 == "幫" and 韻系 in 非敷奉微_韻系:
                        if 聲母 == "明" and 韻系 == "尤":
                            return ""
                        return "w" if 韻腹 != "u" else ""
                    if 組 in "知章莊":
                        if 聲母 == "娘":
                            return 三四等默認
                        if 組 in "知章" and 攝 == "流":
                            return "j"
                        return ""
                    if 組 == "日":
                        if 攝 == "止" and 呼 == "開" or 攝 in "遇效宕咸":
                            return ""
                    return 三四等默認
                case "四":
                    return 三四等默認
        case "合":
            # 規律：除幫組外 i 韻（止蟹）必有 w
            match 組:
                case "幫":
                    return ""
                case val if val in "端知莊章":
                    if 韻 == "i":  # 等價於 韻腹 == "i"
                        return "w"
                    return ""
                case val if val in "來精":
                    if 韻 == "i":
                        return "w"
                    if 攝 == "山" and 等 in "三四":
                        return "ɥ"
                    return ""
                case "日":
                    if 攝 in "止蟹":  # *nɥi > lwi
                        return "w"
                    if 攝 == "臻":  # *nɥun > lun
                        return ""
                    return "ɥ"
                case "見":
                    if 聲母 == "疑" and 攝 == "果":  # 爲修正 訛臥
                        return ""
                    if 攝 == "果" and 等 == "三":  # 爲修正 瘸
                        return "j"
                    if 韻腹 in "aɛ" or 韻 in list("io"):  # 假果止蟹
                        return "w"
                    if 攝 == "宕":
                        return "w"
                    if 攝 == "山":
                        match 等:
                            case "一" | "二":
                                return "w"
                            case "三" | "四":
                                return "ɥ"
                    if 攝 == "臻":
                        match 等:
                            case "一":
                                return ""
                            case "三":
                                return "ɥ" if 韻腹 not in list("uy") else ""
                    if 攝 == "梗" and 等 in "三四":
                        return "j"
                    return ""
                case "影":
                    match 等:
                        case "一" | "二":
                            return "w" if 韻腹 != "u" else ""  # 可能 > f
                        case "三" | "四":
                            if 韻 == "i":
                                return "w"
                            if 攝 == "宕":
                                return "w"
                            if 攝 == "梗":
                                return "j"  # juŋ
                            if 攝 == "果":
                                return "j"  # 爲修正 靴
                            if 攝 in "山":
                                return "ɥ"
                            if 攝 == "臻":
                                return "ɥ" if 韻腹 not in list("uy") else ""
                            return ""
    raise Exception("介音 not found!")


def 推導韻腹(攝: str, 韻系: str, 等: str, 呼: str, 組: str, 聲母: str) -> str:
    if 攝 == "深" and 組 == "莊":
        return "ɛ"  # 可能非本音
    if 韻系 == "元":
        match 呼:
            case "開":
                return "ɛ"  # 只有 見影
            case "合":
                if 組 == "幫":
                    return "a"
                return "o"  # 只有 見影

    match 攝:
        case "通":
            return "u"
        case val if val in "江果宕":
            return "o"
        case val if val in "深":
            return "i"
        case val if val in "假":
            return "a"
        case "止":
            if 組 == "日" and 呼 == "開":
                return "ɛ"
            if 組 in "精莊" and 呼 == "開":
                return "ɿ"
            if 組 == "莊" and 呼 == "合":
                return "a"  # 爲修正 帥率衰揣
            return "i"
        case "遇":
            if 聲母 == "日":
                return "ɛ"
            if 等 == "三" and (組 in "來精見影" or 聲母 == "娘"):
                return "i"
            return "u"
        case "蟹":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            if 組 == "幫":
                                return "i"
                            if 組 in "見影":
                                return "o"
                            return "a"
                        case "合":
                            return "i"  # 白讀 oi
                case "二":
                    return "a"
                case "三" | "四":
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
        case "山":
            match 等:
                case "一" | "二":
                    if 等 == "一":
                        if (呼 == "開" and 組 in "幫見影") or 呼 == "合":
                            return "o"
                    return "a"
                case "三" | "四":
                    match 呼:
                        case "開":
                            return "ɛ"
                        case "合":
                            return "o"
        case "效":
            if (組 in "知章" or 聲母 == "日") and 等 == "三":
                return "ɛ"
            return "a"
        case "梗":  # 白讀 a
            match 等:
                case "二":
                    return "ɛ"
                case "三" | "四":
                    match 呼:
                        case "開":
                            if 組 == "莊":
                                return "ɛ"
                            return "i"
                        case "合":
                            return "u"
        case "曾":
            match 等:
                case "一":
                    return "ɛ"
                case "三":
                    if 組 == "莊":
                        return "ɛ"
                    return "i"
        case "流":
            match 等:
                case "一":
                    return "ɛ"
                case "三":
                    if 聲母 == "明" and 韻系 == "尤":
                        return "ɛ"
                    if 組 == "莊":
                        return "ɛ"
                    return "u"
        case "咸":
            match 等:
                case "一" | "二":
                    if 等 == "一" and 呼 == "開" and 組 in "見影":
                        return "o"
                    return "a"
                case "三" | "四":
                    if 等 == "三" and 呼 == "合":
                        return "a"
                    else:
                        return "ɛ"
    raise Exception("韻腹 not found!")


def 推導韻尾(攝: str, 聲調: str, 韻腹: str) -> str:
    match 攝:
        case val if val in "止遇果假":
            return ""
        case val if val in "深咸臻山":
            return "t" if 聲調 == "入" else "n"
        case val if val in "通江宕":
            return "ʔ" if 聲調 == "入" else "ŋ"
        case "效":
            return "u"
        case "流":
            return "u" if 韻腹 != "u" else ""
        case "梗":
            if 聲調 == "入":
                return "ʔ"
            else:
                if 韻腹 in list("ɛi"):
                    return "n"
                return "ŋ"
        case "曾":
            return "ʔ" if 聲調 == "入" else "n"
        case "蟹":
            return "i" if 韻腹 != "i" else ""  # 例外：話佳娃挂卦
    raise Exception("韻尾 not found!")


def 推導聲調(聲調: str, 清濁: str) -> str:
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


def 推導撫州話(小韻: dict[str, str]) -> dict[str, str]:
    def call_by_dict(func, params):
        sig = inspect.signature(func)
        filtered = {k: v for k, v in params.items() if k in sig.parameters}
        return func(**filtered)

    parts = ["韻腹", "韻尾", "介音", "聲母", "聲調"]  # 不可更改順序！
    try:
        for part in parts:
            小韻[part] = call_by_dict(globals()[f"推導{part}"], 小韻)
    except Exception as e:
        print(小韻["小韻號"], {part: 小韻[part] for part in parts if part in 小韻})
        raise Exception("Error in 推導撫州話:", e)

    # 特殊情況：非敷奉微；曉匣合口 hw > f
    if 小韻["聲母"] == "f" and 小韻["介音"] == "w":
        小韻["介音"] = ""
    if 小韻["聲母"] == "w":
        小韻["聲母"] = ""
        小韻["介音"] = "w" if 小韻["韻腹"] != "u" else ""

    # 爲修正 帥率衰揣
    if 小韻["組"] == "莊" and 小韻["攝"] == "止" and 小韻["呼"] == "合":
        小韻["韻尾"] = "i"

    # 爲修正 梗曾三合入 疫域
    if 小韻["小韻號"] in [3715, 3662]:
        小韻["介音"] = ""
        小韻["韻腹"] = "y"

    return {part: 小韻[part] for part in parts}
