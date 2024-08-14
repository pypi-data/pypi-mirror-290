from smartdiffusion import utils


class ImageScaleBy:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "scale_by": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.01, "max": 8.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"

    CATEGORY = "image/upscaling"

    def upscale(self, image, upscale_method, scale_by):
        samples = image.movedim(-1, 1)
        return (
            common_upscale(
                samples,
                round(samples.shape[3] * scale_by),
                round(samples.shape[2] * scale_by),
                upscale_method,
                "disabled",
            ).movedim(1, -1),
        )
