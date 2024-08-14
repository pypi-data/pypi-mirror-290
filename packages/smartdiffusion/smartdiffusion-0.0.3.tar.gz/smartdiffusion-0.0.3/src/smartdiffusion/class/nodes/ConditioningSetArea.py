from smartdiffusion.config import MAX_RESOLUTION
from smartdiffusion.node_helpers import conditioning_set_values


class ConditioningSetArea:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "width": (
                    "INT",
                    {"default": 64, "min": 64, "max": MAX_RESOLUTION, "step": 8},
                ),
                "height": (
                    "INT",
                    {"default": 64, "min": 64, "max": MAX_RESOLUTION, "step": 8},
                ),
                "x": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "y": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
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
                    "area": (height // 8, width // 8, y // 8, x // 8),
                    "strength": strength,
                    "set_area_to_bounds": False,
                },
            ),
        )
