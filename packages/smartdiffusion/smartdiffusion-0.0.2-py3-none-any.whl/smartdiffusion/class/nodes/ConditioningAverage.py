from torch import cat, zeros, mul
from logging import warning


class ConditioningAverage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning_to": ("CONDITIONING",),
                "conditioning_from": ("CONDITIONING",),
                "conditioning_to_strength": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "addWeighted"

    CATEGORY = "conditioning"

    def addWeighted(self, conditioning_to, conditioning_from, conditioning_to_strength):
        out = []

        if len(conditioning_from) > 1:
            warning(
                "Warning: ConditioningAverage conditioning_from contains more than 1"
                + " cond, only the first one will actually be applied to conditioning_to."
            )
        cond_from = conditioning_from[0][0]
        pooled_output_from = conditioning_from[0][1].get("pooled_output", None)

        for i in range(len(conditioning_to)):
            t1 = conditioning_to[i][0]
            pooled_output_to = conditioning_to[i][1].get(
                "pooled_output", pooled_output_from
            )
            t0 = cond_from[:, : t1.shape[1]]
            if t0.shape[1] < t1.shape[1]:
                t0 = cat(
                    [t0] + [zeros((1, (t1.shape[1] - t0.shape[1]), t1.shape[2]))],
                    dim=1,
                )
            tw = mul(t1, conditioning_to_strength) + mul(
                t0, (1.0 - conditioning_to_strength)
            )
            t_to = conditioning_to[i][1].copy()
            if pooled_output_from is not None and pooled_output_to is not None:
                t_to["pooled_output"] = mul(
                    pooled_output_to, conditioning_to_strength
                ) + mul(pooled_output_from, (1.0 - conditioning_to_strength))
            elif pooled_output_from is not None:
                t_to["pooled_output"] = pooled_output_from
            n = [tw, t_to]
            out.append(n)
        return (out,)
