from smartdiffusion.sd import load_checkpoint_guess_config
from smartdiffusion.folder_paths import (
    get_filename_list,
    get_full_path,
    get_folder_paths,
)


class unCLIPCheckpointLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": (get_filename_list("checkpoints"),),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "CLIP_VISION")
    FUNCTION = "load_checkpoint"

    CATEGORY = "loaders"

    def load_checkpoint(self, ckpt_name, output_vae=True, output_clip=True):
        return load_checkpoint_guess_config(
            get_full_path("checkpoints", ckpt_name),
            output_vae=True,
            output_clip=True,
            output_clipvision=True,
            embedding_directory=get_folder_paths("embeddings"),
        )
