from torch import ones, float32, zeros
from smartdiffusion.config import MAX_RESOLUTION


class ImagePadForOutpaint:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "top": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "right": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "bottom": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8},
                ),
                "feathering": (
                    "INT",
                    {"default": 40, "min": 0, "max": MAX_RESOLUTION, "step": 1},
                ),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "expand_image"

    CATEGORY = "image"

    def expand_image(self, image, left, top, right, bottom, feathering):
        d1, d2, d3, d4 = image.size()

        new_image = (
            ones(
                (d1, d2 + top + bottom, d3 + left + right, d4),
                dtype=float32,
            )
            * 0.5
        )

        new_image[:, top : top + d2, left : left + d3, :] = image

        mask = ones(
            (d2 + top + bottom, d3 + left + right),
            dtype=float32,
        )

        t = zeros((d2, d3), dtype=float32)

        if feathering > 0 and feathering * 2 < d2 and feathering * 2 < d3:

            for i in range(d2):
                for j in range(d3):
                    dt = i if top != 0 else d2
                    db = d2 - i if bottom != 0 else d2

                    dl = j if left != 0 else d3
                    dr = d3 - j if right != 0 else d3

                    d = min(dt, db, dl, dr)

                    if d >= feathering:
                        continue
                    v = (feathering - d) / feathering

                    t[i, j] = v * v
        mask[top : top + d2, left : left + d3] = t

        return (new_image, mask)
