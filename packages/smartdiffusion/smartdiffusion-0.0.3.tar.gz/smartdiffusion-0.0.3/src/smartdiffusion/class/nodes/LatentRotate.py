from torch import rot90


class LatentRotate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "rotation": (["none", "90 degrees", "180 degrees", "270 degrees"],),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "rotate"

    CATEGORY = "latent/transform"

    def rotate(self, samples, rotation):
        s = samples.copy()
        rotate_by = 0
        if rotation.startswith("90"):
            rotate_by = 1
        elif rotation.startswith("180"):
            rotate_by = 2
        elif rotation.startswith("270"):
            rotate_by = 3
        s["samples"] = rot90(samples["samples"], k=rotate_by, dims=[3, 2])
        return (s,)
