from torch.nn.functional import interpolate, conv2d
from torch import ones, clamp
from math import ceil


class VAEEncodeForInpaint:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pixels": ("IMAGE",),
                "vae": ("VAE",),
                "mask": ("MASK",),
                "grow_mask_by": ("INT", {"default": 6, "min": 0, "max": 64, "step": 1}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "encode"

    CATEGORY = "latent/inpaint"

    def encode(self, vae, pixels, mask, grow_mask_by=6):
        x = (pixels.shape[1] // vae.downscale_ratio) * vae.downscale_ratio
        y = (pixels.shape[2] // vae.downscale_ratio) * vae.downscale_ratio
        mask = interpolate(
            mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])),
            size=(pixels.shape[1], pixels.shape[2]),
            mode="bilinear",
        )

        pixels = pixels.clone()
        if pixels.shape[1] != x or pixels.shape[2] != y:
            x_offset = (pixels.shape[1] % vae.downscale_ratio) // 2
            y_offset = (pixels.shape[2] % vae.downscale_ratio) // 2
            pixels = pixels[:, x_offset : x + x_offset, y_offset : y + y_offset, :]
            mask = mask[:, :, x_offset : x + x_offset, y_offset : y + y_offset]
        # grow mask by a few pixels to keep things seamless in latent space

        if grow_mask_by == 0:
            mask_erosion = mask
        else:
            kernel_tensor = ones((1, 1, grow_mask_by, grow_mask_by))
            padding = ceil((grow_mask_by - 1) / 2)

            mask_erosion = clamp(
                conv2d(mask.round(), kernel_tensor, padding=padding),
                0,
                1,
            )
        m = (1.0 - mask.round()).squeeze(1)
        for i in range(3):
            pixels[:, :, :, i] -= 0.5
            pixels[:, :, :, i] *= m
            pixels[:, :, :, i] += 0.5
        t = vae.encode(pixels)

        return ({"samples": t, "noise_mask": (mask_erosion[:, :, :x, :y].round())},)
