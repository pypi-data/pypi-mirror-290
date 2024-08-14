class unCLIPConditioning:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "clip_vision_output": ("CLIP_VISION_OUTPUT",),
                "strength": (
                    "FLOAT",
                    {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "noise_augmentation": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "apply_adm"

    CATEGORY = "conditioning"

    def apply_adm(self, conditioning, clip_vision_output, strength, noise_augmentation):
        if strength == 0:
            return (conditioning,)
        c = []
        for t in conditioning:
            o = t[1].copy()
            x = {
                "clip_vision_output": clip_vision_output,
                "strength": strength,
                "noise_augmentation": noise_augmentation,
            }
            if "unclip_conditioning" in o:
                o["unclip_conditioning"] = o["unclip_conditioning"][:] + [x]
            else:
                o["unclip_conditioning"] = [x]
            n = [t[0], o]
            c.append(n)
        return (c,)
