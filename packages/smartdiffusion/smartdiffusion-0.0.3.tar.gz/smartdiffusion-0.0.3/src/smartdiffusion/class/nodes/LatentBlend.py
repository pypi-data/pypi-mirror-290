from smartdiffusion.utils import common_upscale


class LatentBlend:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples1": ("LATENT",),
                "samples2": ("LATENT",),
                "blend_factor": (
                    "FLOAT",
                    {"default": 0.5, "min": 0, "max": 1, "step": 0.01},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "blend"

    CATEGORY = "_for_testing"

    def blend(
        self, samples1, samples2, blend_factor: float, blend_mode: str = "normal"
    ):

        samples_out = samples1.copy()
        samples1 = samples1["samples"]
        samples2 = samples2["samples"]

        if samples1.shape != samples2.shape:
            samples2.permute(0, 3, 1, 2)
            samples2 = common_upscale(
                samples2, samples1.shape[3], samples1.shape[2], "bicubic", crop="center"
            )
            samples2.permute(0, 2, 3, 1)
        samples_blended = self.blend_mode(samples1, samples2, blend_mode)
        samples_blended = samples1 * blend_factor + samples_blended * (1 - blend_factor)
        samples_out["samples"] = samples_blended
        return (samples_out,)

    def blend_mode(self, img1, img2, mode):
        if mode == "normal":
            return img2
        else:
            raise ValueError(f"Unsupported blend mode: {mode}")
