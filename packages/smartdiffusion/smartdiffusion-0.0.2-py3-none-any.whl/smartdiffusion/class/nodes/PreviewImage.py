from random import choice
from smartdiffusion.folder_paths import folder_paths


class PreviewImage(SaveImage):
    def __init__(self):
        self.output_dir = get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + "".join(
            choice("abcdefghijklmnopqrstupvxyz") for x in range(5)
        )
        self.compress_level = 1

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }
