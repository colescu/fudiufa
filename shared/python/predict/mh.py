"""
（草稿版）
最後更新：2025 年 8 月 21 日
"""

import inspect

from .constants import 非敷奉微_韻系


def 推導聲母(
    聲母: str, 介音: str, 韻腹: str, 韻系: str, 攝: str, 等: str, 呼: str
) -> str:
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
                return "w"
            return "m"
        case "端":
            return "t"
        case "透" | "定":
            return "tʰ"
        case "知" | "精" | "章" | "莊":
            # 例外：知中啄琢 t
            # 例外：上臭 h 支車 k
            return "ts"
        case "徹" | "澄" | "清" | "從" | "昌" | "初" | "崇":
            # 從崇 有些是 s
            return "tsʰ"
        case "泥" | "娘":
            if 介音 == "j" or 介音 == "" and 韻腹 == "i":
                return "ŋ"  # ɲ = ŋj
            return "n"
        case "來":
            return "l"
        case "心" | "邪" | "生" | "俟" | "常" | "書" | "船":
            # 邪生常書 很多 tsʰ TODO
            return "s"
        case "日":
            # 很多無 j
            return "ŋ"
        case "見":
            # 很多 kʰ
            return "k"
        case "溪" | "羣":
            # 很多 h, f
            return "kʰ"
        case "疑":
            return "ŋ"
        case "影" | "云" | "以":
            return ""
        case "曉" | "匣":
            # 很多 k, kʰ
            match 等:
                case "一" | "二":
                    if 是合口:  # 白讀 w
                        return "f"
                    return "h"
                case "三" | "四":
                    if 呼 == "合" and 韻腹 == "i":
                        return "f"
                    if 攝 == "宕" and 呼 == "合":  # 爲修正 況戄 等
                        return "f"
                    return "h"
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
                    if 等 == "二" and 組 in "見影" and 攝 in "蟹山":
                        return "j"
                    return ""
                    # 例外：一等但有 j 嵌暫夾蘸鹼
                case "三":
                    if 組 == "幫" and 韻系 in 非敷奉微_韻系:
                        return "w" if 韻腹 != "u" else ""
                    if 組 in "知章莊":
                        if 聲母 == "娘":
                            return 三四等默認
                        return ""
                    if 組 == "日":
                        return "j" if 韻腹 != "i" else ""
                    return 三四等默認
                case "四":
                    return 三四等默認
                    # 梗攝四等白讀是 ang 而非 iang（例外：醒壁 不確定是否與聲母有關）
        case "合":
            # 規律：除幫組外 i 韻（止蟹）必有 w
            match 組:
                case "幫":
                    return ""
                case val if val in "端知莊章":
                    if 攝 == "臻" and 等 == "三":
                        return ""
                    if 韻 == "i":  # 等價於 韻腹 == "i"
                        return "w"
                    return ""
                case val if val in "來精":
                    if 攝 == "臻" and 等 == "三":
                        return ""
                    if 韻 == "i":
                        return "w"  # 精組 白讀 無 w
                    if 攝 == "山" and 等 in "三四":
                        return "j"
                    return ""
                case "日":
                    return "j" if 韻腹 != "i" else ""
                case "見":
                    if 聲母 == "疑" and 攝 == "果":  # 爲修正 訛臥
                        return ""
                    if 攝 == "果" and 等 == "三":  # 爲修正 瘸
                        return "j"
                    if 韻腹 in "ae" or 韻 in list("io"):  # 假果止蟹
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
                                return "j"
                    if 攝 == "梗" and 等 in "三四":  # 梗曾 字少
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
                                return "j"
                            if 攝 in "山果":
                                return "j"
                            if 攝 == "臻":
                                return "j"
                            return ""
    raise Exception("介音 not found!")


# 不同：w > v，kwong -> kong，ɥon > jan/jen


def 推導韻腹(攝: str, 韻系: str, 等: str, 呼: str, 組: str, 聲母: str):
    if 韻系 == "元":
        return "a"  # 例外：發翻阮 on 掘 kʰjut 喧 sjen

    match 攝:
        case "通":
            return "u"  # 例外：沃浴福 ok
        case "江":
            return "o"  # 例外：窗雙棒濁虹 uŋ 層
        case "止":
            if 組 in "知章精莊" and 聲母 != "娘":
                return "ɿ"
            return "i"  # 四死姊肆 CORRECTION!!!
            # 例外：開口 徙滓璽（讀若蟹三四） 你 n 知 ti 支 ki
            # 合口 吹炊睡嘴衰 oi（無規律） 綏 se
        case "遇":
            # 例外讀鼻音 n：五伍吾梧午吳蜈女魚漁（一三等都有）
            # 其他例外雜亂
            if 組 in "精莊":
                return "ɿ"
            if 等 == "三" and (組 in "來日精見影" or 聲母 == "娘"):
                return "i"
            return "u"  # 三等即幫知章
        case "蟹":
            match 等:
                case "一":
                    match 呼:
                        case "開":
                            if 組 == "幫":
                                return "i"
                            if 組 in "見影":
                                return "o"
                            return "a"  # FIXME 很多 o 無規律
                        case "合":
                            return "i"  # 白讀 oi
                case "二":
                    return "a"  # 例外：楷 kʰoi 篩 sɿ
                case "三" | "四":
                    if 組 in "章精" and 呼 == "開":
                        return "ɿ"
                    return "i"  # 合口有些白讀 oi
                    # 例外：世歲滯繫婿洗砌細齊係契雞 e 黎低底弟啼蹄泥溪 ai 梯 oi
        case "臻":
            match 等:
                case "一":
                    if 組 == "端":  # 端臻一開僅有 吞
                        return "u"
                    match 呼:
                        case "開":
                            return "e"
                        case "合":
                            return "u"  # 例外：崑 ken
                case "三":
                    match 呼:
                        case "開":
                            if 組 in "知章":
                                return "ə"
                            return "i"
                            # 例外：僅勤謹韌忍芹近銀隱 iun（上古）
                            # 白讀 密蜜弼憫敏櫛蝨襯閩 e
                            # 乙 jat 份 fun
                        case "合":
                            return "u"  # 例外：律輪恤迅率橘 i（有些 u 也可）
        case "山":
            match 等:
                case "一" | "二":
                    if 等 == "一":
                        if (呼 == "開" and 組 in "幫見影") or (
                            呼 == "合" and 組 != "幫"
                        ):
                            return "o"
                    return "a"
                    # 例外：刊岸 an（岸是唯一疑母字，但安是 on）
                    # 見影好多 a，尤其入聲全是 a TODO
                case "三" | "四":
                    match 呼:
                        case "開":
                            if 組 in "知章見影日":
                                return "a"
                            return "e"
                        case "合":
                            if 組 in "見影":
                                return "a"
                            if 組 in "精":
                                return "e"
                            return "o"
                        # 略混亂
        case "效":
            return "a"
        case "果":
            return "o"  # 例外：我荷跛搓 ai（上古）
        case "假":
            return "a"
        case "宕":
            return "o"
        case "梗":
            match 等:
                case "二":
                    return "e"
                case "三" | "四":
                    match 呼:
                        case "開":
                            if 組 in "知章":
                                return "ə"
                            return "i"
                        # 四等很多讀 e
                        case "合":
                            return "u"
                            # 很多 i 可能是普通話影響
        case "曾":
            match 等:
                case "一":
                    return "e"  # 例外：特肋 it 塞 sat（白讀）
                case "三":
                    if 組 == "莊":
                        return "e"
                    if 組 in "知章" and 聲母 != "娘":
                        return "ə"
                    return "i"
                    # 有些有 e 讀
        case "流":
            match 等:
                case "一":
                    return "e"  # 例外：茂貿剖 jau 剖 pʰo
                case "三":
                    if 組 == "莊":
                        return "e"
                    return "u"  # 例外較多
                    # 見流三白讀 eu
        case "深":
            if 組 in "知章莊":
                return "ə"
            return "i"
        case "咸":
            return "a"  # 例外：含喊墊臉貶鵪砍賺
    raise Exception("韻腹 not found!")


def 推導韻尾(攝: str, 聲調: str, 韻腹: str) -> str:
    """
    例外：
    上古層 止開 ai 果 ai
    白讀層 止合 oi

    個別例外：
    臂避 i/it 募塑錯 u/ok 區箍縷 eu 姆 me
    深咸：圳 tsun 蟄 tsʰət 品 pʰin 賺 tsʰon
    臻山：潷 bi 頁 jap 蟬 sam
    梗曾：易億 it
    """

    match 攝:
        case val if val in "止遇果假":
            return ""
        case val if val in "深咸":
            return "p" if 聲調 == "入" else "m"
        case val if val in "臻山":
            return "t" if 聲調 == "入" else "n"
        case val if val in "通江宕":
            return "k" if 聲調 == "入" else "ŋ"
        case "效":
            return "u"
        case "流":
            return "u" if 韻腹 != "u" else ""
        case "梗":
            if 聲調 == "入":
                return "k"  # 無白讀
            else:
                if 韻腹 in list("eiə"):
                    return "n"  # 白讀 ŋ
                return "ŋ"
        case "曾":
            return "t" if 聲調 == "入" else "n"
        case "蟹":
            return "i" if 韻腹 not in list("iɿe") else ""  # 例外：話佳娃挂卦
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
                    return "5"  # 多歸陰平
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
                    return "7"  # 例外多
    raise Exception("聲調 not found!")


def 推導梅縣話(小韻: dict[str, str]) -> dict[str, str]:
    def call_by_dict(func, params):
        sig = inspect.signature(func)
        filtered = {k: v for k, v in params.items() if k in sig.parameters}
        return func(**filtered)

    parts = ["韻腹", "韻尾", "介音", "聲母", "聲調"]  # The order is important!
    try:
        for part in parts:
            小韻[part] = call_by_dict(globals()[f"推導{part}"], 小韻)
    except Exception as e:
        print(小韻["小韻號"], {part: 小韻[part] for part in parts if part in 小韻})
        raise Exception("Error in 推導梅縣話:", e)

    # 特殊情況：非敷奉微；曉蝦 hw > f
    if 小韻["聲母"] == "f" and 小韻["介音"] == "w":
        小韻["介音"] = ""
    if 小韻["聲母"] == "w":
        小韻["聲母"] = ""
        小韻["介音"] = "w" if 小韻["韻腹"] != "u" else ""
    if 小韻["聲母"] == "" and 小韻["介音"] == "w":
        小韻["介音"] = ""
        小韻["聲母"] = "v"

    return {part: 小韻[part] for part in parts}
