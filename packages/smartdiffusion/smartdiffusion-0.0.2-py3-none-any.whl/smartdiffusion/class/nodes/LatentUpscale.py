from smartdiffusion.utils import common_upscale
from smartdiffusion.config import MAX_RESOLUTION


class LatentUpscale:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]
    crop_methods = ["disabled", "center"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "upscale_method": (s.upscale_methods,),
                "width": (
                    "INT",
                    {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "crop": (s.crop_methods,),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "upscale"

    CATEGORY = "latent"

    def upscale(self, samples, upscale_method, width, height, crop):
        if width == 0 and height == 0:
            s = samples
        else:
            s = samples.copy()

            if width == 0:
                height = max(64, height)
                width = max(
                    64,
                    round(
                        samples["samples"].shape[3]
                        * height
                        / samples["samples"].shape[2]
                    ),
                )
            elif height == 0:
                width = max(64, width)
                height = max(
                    64,
                    round(
                        samples["samples"].shape[2]
                        * width
                        / samples["samples"].shape[3]
                    ),
                )
            else:
                width = max(64, width)
                height = max(64, height)
            s["samples"] = common_upscale(
                samples["samples"], width // 8, height // 8, upscale_method, crop
            )
        return (s,)
