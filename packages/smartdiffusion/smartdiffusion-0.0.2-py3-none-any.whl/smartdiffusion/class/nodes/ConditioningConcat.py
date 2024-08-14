from torch import cat
from logging import warning


class ConditioningConcat:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning_to": ("CONDITIONING",),
                "conditioning_from": ("CONDITIONING",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "concat"

    CATEGORY = "conditioning"

    def concat(self, conditioning_to, conditioning_from):
        out = []

        if len(conditioning_from) > 1:
            warning(
                "Warning: ConditioningConcat conditioning_from contains more than 1"
                + " cond, only the first one will actually be applied to conditioning_to."
            )
        cond_from = conditioning_from[0][0]

        for i in range(len(conditioning_to)):
            t1 = conditioning_to[i][0]
            tw = cat((t1, cond_from), 1)
            n = [tw, conditioning_to[i][1].copy()]
            out.append(n)
        return (out,)
