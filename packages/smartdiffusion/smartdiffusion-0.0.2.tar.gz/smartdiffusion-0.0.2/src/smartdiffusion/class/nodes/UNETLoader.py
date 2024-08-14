from torch import float8_e4m3fn, float8_e5m2
from smartdiffusion.sd import load_unet
from smartdiffusion.folder_paths import get_full_path, get_filename_list


class UNETLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "unet_name": (get_filename_list("unet"),),
                "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e5m2"],),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load_unet"

    CATEGORY = "advanced/loaders"

    def load_unet(self, unet_name, weight_dtype, path="unet"):
        if weight_dtype == "fp8_e4m3fn":
            dtype = float8_e4m3fn
        elif weight_dtype == "fp8_e5m2":
            dtype = float8_e5m2
        return (load_unet(get_full_path(path, unet_name), dtype=dtype),)
