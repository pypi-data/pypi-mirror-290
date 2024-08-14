from torch import full, cat
from smartdiffusion.config import MAX_RESOLUTION


class EmptyImage:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": (
                    "INT",
                    {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1},
                ),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                "color": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFF,
                        "step": 1,
                        "display": "color",
                    },
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"

    CATEGORY = "image"

    def generate(self, width, height, batch_size=1, color=0):
        r = full([batch_size, height, width, 1], ((color >> 16) & 0xFF) / 0xFF)
        g = full([batch_size, height, width, 1], ((color >> 8) & 0xFF) / 0xFF)
        b = full([batch_size, height, width, 1], ((color) & 0xFF) / 0xFF)
        return (cat((r, g, b), dim=-1),)
