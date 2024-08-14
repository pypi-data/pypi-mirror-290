from smartdiffusion.utils import common_upscale


class LatentUpscaleBy:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "upscale_method": (s.upscale_methods,),
                "scale_by": (
                    "FLOAT",
                    {"default": 1.5, "min": 0.01, "max": 8.0, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "upscale"

    CATEGORY = "latent"

    def upscale(self, samples, upscale_method, scale_by):
        s = samples.copy()
        s["samples"] = common_upscale(
            samples["samples"],
            round(samples["samples"].shape[3] * scale_by),
            round(samples["samples"].shape[2] * scale_by),
            upscale_method,
            "disabled",
        )
        return (s,)
