from smartdiffusion.node_helpers import conditioning_set_values


class ConditioningSetAreaPercentage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "width": (
                    "FLOAT",
                    {"default": 1.0, "min": 0, "max": 1.0, "step": 0.01},
                ),
                "height": (
                    "FLOAT",
                    {"default": 1.0, "min": 0, "max": 1.0, "step": 0.01},
                ),
                "x": ("FLOAT", {"default": 0, "min": 0, "max": 1.0, "step": 0.01}),
                "y": ("FLOAT", {"default": 0, "min": 0, "max": 1.0, "step": 0.01}),
                "strength": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "append"

    CATEGORY = "conditioning"

    def append(self, conditioning, width, height, x, y, strength):
        return (
            conditioning_set_values(
                conditioning,
                {
                    "area": ("percentage", height, width, y, x),
                    "strength": strength,
                    "set_area_to_bounds": False,
                },
            ),
        )
