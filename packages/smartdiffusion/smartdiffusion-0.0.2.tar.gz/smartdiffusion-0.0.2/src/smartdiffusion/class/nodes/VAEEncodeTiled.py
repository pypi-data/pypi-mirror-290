class VAEEncodeTiled:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pixels": ("IMAGE",),
                "vae": ("VAE",),
                "tile_size": (
                    "INT",
                    {"default": 512, "min": 320, "max": 4096, "step": 64},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "encode"

    CATEGORY = "_for_testing"

    def encode(self, vae, pixels, tile_size):
        return (
            {
                "samples": vae.encode_tiled(
                    pixels[:, :, :, :3],
                    tile_x=tile_size,
                    tile_y=tile_size,
                )
            },
        )
