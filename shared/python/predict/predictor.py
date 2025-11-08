import inspect


PARTS = ["聲母", "介音", "韻腹", "韻尾", "韻", "韻母", "聲調"]


class Predictor:
    def __init__(
        self,
        module,
        name: str,
        parts: list[str] = [
            "韻腹",
            "韻尾",
            "介音",
            "聲母",
            "聲調",
        ],  # The order is important
    ):
        self.name = name
        self.parts = parts
        self.utils = {
            **{part: module.get(f"推導{part}", lambda *_: "") for part in self.parts},
            "normalize": module.get("normalize", lambda _: None),
        }

    @staticmethod
    def _call_by_dict(func, params):
        sig = inspect.signature(func)
        filtered = {k: v for k, v in params.items() if k in sig.parameters}
        return func(**filtered)

    def predict(self, 小韻: dict[str, str]) -> str:  # in raw IPA
        try:
            for part in self.parts:
                小韻[part] = self._call_by_dict(self.utils[part], 小韻)
        except Exception as e:
            print(
                小韻["小韻號"],
                {part: 小韻[part] for part in self.parts if part in 小韻},
            )
            raise Exception(f"Error in 推導{self.name}:", e)

        self.utils["normalize"](小韻)

        return "".join([小韻[part] for part in PARTS if part in self.parts])
