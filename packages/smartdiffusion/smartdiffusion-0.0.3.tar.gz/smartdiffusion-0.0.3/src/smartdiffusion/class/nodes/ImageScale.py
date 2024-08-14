from smartdiffusion.utils import common_upscale
from smartdiffusion.config import MAX_RESOLUTION


class ImageScale:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    crop_methods = ["disabled", "center"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "width": (
                    "INT",
                    {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1},
                ),
                "crop": (s.crop_methods,),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"

    CATEGORY = "image/upscaling"

    def upscale(self, image, upscale_method, width, height, crop):
        if width == 0 and height == 0:
            s = image
        else:
            samples = image.movedim(-1, 1)

            if width == 0:
                width = max(1, round(samples.shape[3] * height / samples.shape[2]))
            elif height == 0:
                height = max(1, round(samples.shape[2] * width / samples.shape[3]))
            s = common_upscale(samples, width, height, upscale_method, crop)
            s = s.movedim(1, -1)
        return (s,)
