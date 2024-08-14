from smartdiffusion.node_helpers import conditioning_set_values


class ConditioningSetMask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "mask": ("MASK",),
                "strength": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "set_cond_area": (["default", "mask bounds"],),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "append"

    CATEGORY = "conditioning"

    def append(self, conditioning, mask, set_cond_area, strength):
        return (
            conditioning_set_values(
                conditioning,
                {
                    "mask": mask.unsqueeze(0) if len(mask.shape) < 3 else mask,
                    "set_area_to_bounds": set_cond_area != "default",
                    "mask_strength": strength,
                },
            ),
        )
