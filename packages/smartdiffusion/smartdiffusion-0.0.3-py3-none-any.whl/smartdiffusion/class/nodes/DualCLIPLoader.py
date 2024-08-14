from smartdiffusion.sd import CLIPType, load_clip
from smartdiffusion.folder_paths import (
    get_filename_list,
    get_full_path,
    get_folder_paths,
)


class DualCLIPLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip_name1": (get_filename_list("clip"),),
                "clip_name2": (get_filename_list("clip"),),
                "type": (["sdxl", "sd3", "flux"],),
            }
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "load_clip"

    CATEGORY = "advanced/loaders"

    def load_clip(self, clip_name1, clip_name2, type):
        clip_path1 = get_full_path("clip", clip_name1)
        if type == "sdxl":
            clip_type = CLIPType.STABLE_DIFFUSION
            clip_path2 = get_full_path("clip", clip_name2)
        elif type == "sd3":
            clip_type = CLIPType.SD3
            clip_path2 = get_full_path("t5", clip_name2)
        elif type == "flux":
            clip_type = CLIPType.FLUX
            clip_path2 = get_full_path("t5", clip_name2)
        return (
            load_clip(
                ckpt_paths=[clip_path1, clip_path2],
                embedding_directory=get_folder_paths("embeddings"),
                clip_type=clip_type,
            ),
        )
