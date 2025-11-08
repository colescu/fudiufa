"""
最後更新：2025 年 11 月 8 日
"""

from .predictor import Predictor
from .constants import 非敷奉微_韻系


def 推導聲母(
    聲母: str, 介音: str, 韻腹: str, 韻系: str, 攝: str, 等: str, 呼: str
) -> str:
    是合口 = 介音 == "w" or 介音 == "" and 韻腹 == "u"
    match 聲母:
        # 幫組白讀重脣音
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
                return "v"
            return "m"
        case "端":
            return "t"
        case "透" | "定":
            return "tʰ"
        case "泥" | "娘":
            if 介音 == "j":  # nj > ŋj (但 ni ≠ ŋi)
                return "ŋ"
            return "n"
        case "來":
            return "l"
        # 知組白讀若端組
        case "知" | "精" | "章" | "莊":
            # 例外：上臭 h 支車 k
            return "ts"
        # 很多塞擦音/擦音混亂
        case "徹" | "澄" | "清" | "從" | "昌" | "初" | "崇":
            return "tsʰ"
        case "心" | "邪" | "生" | "俟" | "常" | "書" | "船":
            return "s"
        case "見":
            return "k"
        case "溪" | "羣":
            return "kʰ"
        case "疑" | "日":
            return "ŋ"
        case "影" | "云" | "以":
            return ""
        case "曉" | "匣":
            # 匣母白讀 w (> v)
            if 是合口:
                return "f"
            if 呼 == "合" and 韻腹 == "i":  # 爲修正 梗曾三合 𧵣敻瞁洫 hin > fin
                return "f"
            return "h"
    raise Exception("聲母 not found!")


def 推導介音(
    等: str, 呼: str, 組: str, 聲母: str, 韻系: str, 攝: str, 韻腹: str, 韻尾: str
) -> str:
    if 組 == "幫" and 韻系 in 非敷奉微_韻系:
        return ""

    默認細音 = "j" if 韻腹 not in list("iɿ") else ""
    默認合口 = "w" if 韻腹 not in list("u") else ""
    默認撮口 = "j"  # 無撮口
    match 呼:
        case "" | "開":
            match 等:
                case "一" | "二":
                    if (
                        等 == "二"
                        and 組 == "見"
                        and (
                            (攝 == "蟹" and 聲母 != "疑")  # 街 kjai
                            or 攝 == "山"  # 間 kjan
                        )
                    ):
                        return "j"
                    return ""
                case "三" | "四":
                    if 組 in "知章莊" and 聲母 != "娘":  # 通常丟介音
                        if 組 == "莊" and 攝 in "流通":  # tsju, tsjuŋ
                            return 默認細音
                        return ""
                    return 默認細音
        case "合":
            if 等 in "三四":
                if 聲母 == "日":
                    return 默認細音
                if (
                    攝 == "果"  # 只有見影
                    or (攝 == "山" and 組 in "精見影")
                    or (攝 == "臻" and 組 in "見影")  # 精 俊 zun
                ):  # PM üe, üan, ün
                    return 默認撮口
                if 攝 in "梗曾":  # juŋ 或 wen 或 in
                    return {"u": "j", "e": "w", "i": ""}[韻腹]
                if 聲母 == "以" and 攝 == "蟹":  # 爲修正 銳睿
                    return "j"
            return 默認合口
    raise Exception("介音 not found!")


def 推導韻腹(攝: str, 韻系: str, 等: str, 呼: str, 組: str, 聲母: str, 聲調: str):
    if 韻系 in "元凡":  # (j)an/m
        return "a"  # 例外：發翻阮 on

    match 攝:
        case "假" | "效" | "咸":
            # 咸攝例外：含喊鵪臉 em
            return "a"
        case "果" | "江" | "宕":
            # 上古層
            # 果攝 我荷跛搓 ai
            # 江攝 窗雙棒濁虹 uŋ
            return "o"
        case "通":
            return "u"  # 例外：沃浴福 ok
        case "止":
            if 呼 == "合" and 聲母 == "日":
                return "ui"  # ngiui
            if 呼 == "開" and 組 in "精莊知章" and 聲母 != "娘":
                return "ɿ"
            return "i"
            # 例外：
            # 開口 精組 四死姊肆 i 徙璽滓 ai
            # 合口 吹炊睡嘴衰 oi
        case "遇":
            match 等:
                case "一":
                    if 組 == "精":
                        return "ɿ"
                    return "u"
                case "三":
                    if 組 in "幫知章" and 聲母 != "娘":
                        return "u"
                    if 組 == "莊":
                        return "ɿ"
                    return "i"
            # 例外雜亂
        case "蟹":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            if 組 == "幫":
                                return "i"
                            if 組 in "見影" or 韻系 == "咍":  # 分咍泰
                                return "o"
                            return "a"
                        case "合":
                            return "i"  # 白讀 oi
                case "二":
                    return "a"
                case "三" | "四":
                    if 呼 == "開" and 組 in "知章":
                        return "ɿ"
                    if 呼 == "合" and 聲母 in "日以":
                        return "ui"  # iui
                    return "i"  # 合口白讀 oi ?
                    # 白讀：
                    # 世歲滯繫婿洗砌細齊係契雞 e
                    # 黎低底弟啼蹄泥溪 ai
        case "流":
            match 等:
                case "一":
                    return "e"
                case "三":
                    if 聲母 == "明" and 韻系 == "尤":  # 爲修正 謀牟矛
                        return "e"
                    return "u"
        case "深":
            if 組 in "知章" and 聲母 != "娘":
                return "ə"
            if 組 == "莊":
                return "e"
            return "i"
        case "山":
            match 等:
                case "一" | "二":
                    if (
                        等 == "一"
                        and 組 != "幫"
                        and (
                            (呼 == "開" and 組 in "見影")
                            or (
                                呼 == "合"
                                and not (組 in "見影" and 聲調 == "入")  # 爲修正 活括
                                # CHECK 見影山一合 kwan vs kwon
                            )
                        )
                    ):
                        return "o"
                    return "a"
                case "三" | "四":
                    match 呼:
                        case val if val == "開" or 組 in "精見影":
                            if 組 in (
                                "知章"  # zan
                                # + "見影日"  # jan (allophone of jɛn)
                            ):
                                return "a"
                            return "e"  # jen
                        case "合":  # on
                            return "o"
        case "臻":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            return "e"
                        case "合":
                            return "u"
                case "三":
                    match 呼:
                        case "開":
                            if 組 in "知章" and 聲母 != "娘":
                                return "ə"
                            return "i"
                            # 上古層 僅勤謹韌忍芹近銀隱 iun
                            # 白讀 密蜜弼憫敏櫛蝨襯閩 en
                        case "合":  # iun
                            return "u"  # 例外：律輪恤迅率橘 i
        case "梗" | "曾":
            # 梗攝白讀 a
            match 等:
                case "一" | "二":
                    return "e"
                    # 曾攝例外：特肋 it 塞 sat
                case "三" | "四":
                    match 呼:
                        case "開":
                            if 組 == "莊":
                                return "e"
                            if 組 in "知章" and 聲母 != "娘":
                                return "ə"
                            return "i"
                        case "合":
                            # CHECK 不確定
                            if 韻系 == "清":
                                return "i"  # 普通話影響?
                            if 韻系 in "青蒸":
                                return "e"
                            return "u"
    raise Exception("韻腹 not found!")


def 推導韻尾(攝: str, 聲調: str, 韻腹: str) -> str:
    match 攝:
        case val if val in "止遇果假":
            return ""
        case "蟹":
            return "i" if 韻腹 not in list("ieɿ") else ""
        case val if val in "效流":
            return "u" if 韻腹 != "u" else ""
        case val if val in "深咸":
            return "p" if 聲調 == "入" else "m"
        case val if val in "臻山":
            return "t" if 聲調 == "入" else "n"
        case val if val in "通江宕":
            return "k" if 聲調 == "入" else "ŋ"
        case val if val in "梗曾":
            if 韻腹 in list("eiə"):
                return "n" if 聲調 != "入" else "t"  # 白讀 aŋ/k
            return "ŋ" if 聲調 != "入" else "k"
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
                    return "5"  # 白讀陰平
                case _:
                    return "3"
        case "去":
            return "5"
        case "入":
            match 清濁:
                case "全清" | "次清":
                    return "7"
                case "全濁":
                    return "8"
                case "次濁":
                    return "7"  # FIXME 例外多
    raise Exception("聲調 not found!")


def normalize(小韻):
    if 小韻["聲母"] == "" and (
        小韻["介音"] == "w" or 小韻["介音"] == "" and 小韻["韻腹"] == "u"
    ):  # -w- > v-
        小韻["介音"] = ""
        小韻["聲母"] = "v"
    if 小韻["韻腹"] == "ui":  # jui
        小韻["韻腹"], 小韻["韻尾"] = "u", "i"

    # phonological constraints
    if (
        小韻["介音"] == "j"
        and 小韻["韻腹"] in list("ae")
        and 小韻["韻尾"] in list("nt")
    ):  # jen vs jan
        小韻["韻腹"] = "a" if 小韻["聲母"] in ["k", "kʰ", "ŋ", "h", ""] else "e"
    if 小韻["介音"] == "w" and not (
        小韻["聲母"] in ["k", "kʰ"]
        or (
            小韻["聲母"] in ["t", "tʰ", "n", "l", "ts", "tsʰ", "s", "ŋ"]
            and 小韻["韻腹"] == "i"
            and 小韻["韻尾"] == ""
        )
    ):  # delete -w-
        小韻["介音"] = ""


推導梅縣話 = Predictor(module=globals(), name="梅縣話").predict
