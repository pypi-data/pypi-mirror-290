from smartdiffusion.sd import CLIPType, load_clip
from smartdiffusion.folder_paths import (
    get_filename_list,
    get_full_path,
    get_folder_paths,
)


def __getClipType(type):
    if type == "stable_cascade":
        return CLIPType.STABLE_CASCADE
    if type == "sd3":
        return CLIPType.SD3
    if type == "stable_audio":
        return CLIPType.STABLE_AUDIO
    return CLIPType.STABLE_DIFFUSION


class CLIPLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip_name": (get_filename_list("clip"),),
                "type": (
                    ["stable_diffusion", "stable_cascade", "sd3", "stable_audio"],
                ),
            }
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "load_clip"

    CATEGORY = "advanced/loaders"

    def load_clip(self, clip_name, type="stable_diffusion"):
        return (
            load_clip(
                ckpt_paths=[get_full_path("clip", clip_name)],
                embedding_directory=get_folder_paths("embeddings"),
                clip_type=__getClipType(type),
            ),
        )
