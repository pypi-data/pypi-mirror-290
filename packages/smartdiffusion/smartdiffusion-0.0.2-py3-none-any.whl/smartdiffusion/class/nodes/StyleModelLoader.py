from smartdiffusion.sd import load_style_model
from smartdiffusion.folder_paths import get_full_path, get_filename_list


class StyleModelLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"style_model_name": (get_filename_list("style_models"),)}}

    RETURN_TYPES = ("STYLE_MODEL",)
    FUNCTION = "load_style_model"

    CATEGORY = "loaders"

    def load_style_model(self, style_model_name):
        return (load_style_model(get_full_path("style_models", style_model_name)),)
