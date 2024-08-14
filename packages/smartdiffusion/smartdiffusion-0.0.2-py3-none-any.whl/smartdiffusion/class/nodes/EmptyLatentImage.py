from torch import zeros
from smartdiffusion.model_management import intermediate_device
from smartdiffusion.config import MAX_RESOLUTION


class EmptyLatentImage:
    def __init__(self):
        self.device = intermediate_device()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": (
                    "INT",
                    {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8},
                ),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"

    CATEGORY = "latent"

    def generate(self, width, height, batch_size=1):
        return (
            {
                "samples": zeros(
                    [batch_size, 4, height // 8, width // 8], device=self.device
                )
            },
        )
