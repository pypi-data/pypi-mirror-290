from torch import cat


class StyleModelApply:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "style_model": ("STYLE_MODEL",),
                "clip_vision_output": ("CLIP_VISION_OUTPUT",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "apply_stylemodel"

    CATEGORY = "conditioning/style_model"

    def apply_stylemodel(self, clip_vision_output, style_model, conditioning):
        cond = (
            style_model.get_cond(clip_vision_output)
            .flatten(start_dim=0, end_dim=1)
            .unsqueeze(dim=0)
        )
        c = []
        for t in conditioning:
            n = [cat((t[0], cond), dim=1), t[1].copy()]
            c.append(n)
        return (c,)
