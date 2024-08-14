from smartdiffusion.sd import load_checkpoint
from smartdiffusion.folder_paths import (
    get_full_path,
    get_filename_list,
    get_folder_paths,
)


class CheckpointLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "config_name": (get_filename_list("configs"),),
                "ckpt_name": (get_filename_list("checkpoints"),),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_checkpoint"

    CATEGORY = "advanced/loaders"

    def load_checkpoint(self, config_name, ckpt_name):
        return load_checkpoint(
            get_full_path("configs", config_name),
            get_full_path("checkpoints", ckpt_name),
            output_vae=True,
            output_clip=True,
            embedding_directory=get_folder_paths("embeddings"),
        )
