from smartdiffusion.config import MAX_RESOLUTION


class LatentCrop:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "width": (
                    "INT",
                    {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 8},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 8},
                ),
                "x": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "y": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "crop"

    CATEGORY = "latent/transform"

    def crop(self, samples, width, height, x, y):
        s = samples.copy()
        samples = samples["samples"]
        x = x // 8
        y = y // 8

        # enfonce minimum size of 64

        if x > (samples.shape[3] - 8):
            x = samples.shape[3] - 8
        if y > (samples.shape[2] - 8):
            y = samples.shape[2] - 8
        new_height = height // 8
        new_width = width // 8
        to_x = new_width + x
        to_y = new_height + y
        s["samples"] = samples[:, :, y:to_y, x:to_x]
        return (s,)
