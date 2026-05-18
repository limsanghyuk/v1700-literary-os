from v1700.ir.style_profile import StyleProfileIR

class AuthorialVoiceAdapter:
    """Applies abstract style features only; it does not imitate a named author."""

    def apply(self, text: str, style: StyleProfileIR) -> str:
        out = text
        if style.metaphor_policy == "rare_specific":
            out = out.replace("아름답게", "낮게")
        if style.dialogue_policy.startswith("understated"):
            out = out.replace("정말로", "")
        return out
