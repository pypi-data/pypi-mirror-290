from os import path, listdir
from hashlib import sha256
from safetensors.torch import load_file
from smartdiffusion.folder_paths import (
    get_input_directory,
    get_annotated_filepath,
    exists_annotated_filepath,
)


class LoadLatent:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = get_input_directory()
        files = [
            f
            for f in listdir(input_dir)
            if path.isfile(path.join(input_dir, f)) and f.endswith(".latent")
        ]
        return {
            "required": {
                "latent": [
                    sorted(files),
                ]
            },
        }

    CATEGORY = "_for_testing"

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load"

    def load(self, latent):
        latent = load_file(get_annotated_filepath(latent), device="cpu")
        multiplier = 1.0
        if "latent_format_version_0" not in latent:
            multiplier = 1.0 / 0.18215
        return ({"samples": latent["latent_tensor"].float() * multiplier},)

    @classmethod
    def IS_CHANGED(s, latent):
        m = hashlib.sha256()
        with open(get_annotated_filepath(latent), "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, latent):
        if not exists_annotated_filepath(latent):
            return "Invalid latent file: {}".format(latent)
        return True
