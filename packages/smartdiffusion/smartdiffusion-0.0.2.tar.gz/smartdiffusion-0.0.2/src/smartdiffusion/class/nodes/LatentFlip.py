from torch import flip


class LatentFlip:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "flip_method": (["x-axis: vertically", "y-axis: horizontally"],),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "flip"

    CATEGORY = "latent/transform"

    def flip(self, samples, flip_method):
        s = samples.copy()
        if flip_method.startswith("x"):
            s["samples"] = flip(samples["samples"], dims=[2])
        elif flip_method.startswith("y"):
            s["samples"] = flip(samples["samples"], dims=[3])
        return (s,)
