from torch import ones_like
from smartdiffusion.config import MAX_RESOLUTION


class LatentComposite:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples_to": ("LATENT",),
                "samples_from": ("LATENT",),
                "x": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "y": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "feather": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "composite"

    CATEGORY = "latent"

    def composite(
        self, samples_to, samples_from, x, y, composite_method="normal", feather=0
    ):
        x = x // 8
        y = y // 8
        feather = feather // 8
        samples_out = samples_to.copy()
        s = samples_to["samples"].clone()
        samples_to = samples_to["samples"]
        samples_from = samples_from["samples"]
        if feather == 0:
            s[:, :, y : y + samples_from.shape[2], x : x + samples_from.shape[3]] = (
                samples_from[:, :, : samples_to.shape[2] - y, : samples_to.shape[3] - x]
            )
        else:
            samples_from = samples_from[
                :, :, : samples_to.shape[2] - y, : samples_to.shape[3] - x
            ]
            mask = ones_like(samples_from)
            for t in range(feather):
                if y != 0:
                    mask[:, :, t : 1 + t, :] *= (1.0 / feather) * (t + 1)
                if y + samples_from.shape[2] < samples_to.shape[2]:
                    mask[:, :, mask.shape[2] - 1 - t : mask.shape[2] - t, :] *= (
                        1.0 / feather
                    ) * (t + 1)
                if x != 0:
                    mask[:, :, :, t : 1 + t] *= (1.0 / feather) * (t + 1)
                if x + samples_from.shape[3] < samples_to.shape[3]:
                    mask[:, :, :, mask.shape[3] - 1 - t : mask.shape[3] - t] *= (
                        1.0 / feather
                    ) * (t + 1)
            rev_mask = ones_like(mask) - mask
            s[:, :, y : y + samples_from.shape[2], x : x + samples_from.shape[3]] = (
                samples_from[:, :, : samples_to.shape[2] - y, : samples_to.shape[3] - x]
                * mask
                + s[:, :, y : y + samples_from.shape[2], x : x + samples_from.shape[3]]
                * rev_mask
            )
        samples_out["samples"] = s
        return (samples_out,)
