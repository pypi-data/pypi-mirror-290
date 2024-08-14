from os import path
from json import dumps
from smartdiffusion.utils import save_torch_file
from smartdiffusion.cli_args import args
from smartdiffusion.folder_paths import get_output_directory, get_save_image_path


class SaveLatent:
    def __init__(self):
        self.output_dir = get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "filename_prefix": ("STRING", {"default": "latents/smartdiffusionui"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save"

    OUTPUT_NODE = True

    CATEGORY = "_for_testing"

    def save(
        self,
        samples,
        filename_prefix="smartdiffusionui",
        prompt=None,
        extra_pnginfo=None,
    ):
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            get_save_image_path(filename_prefix, self.output_dir)
        )

        # support save metadata for latent sharing

        prompt_info = ""
        if prompt is not None:
            prompt_info = dumps(prompt)
        metadata = None
        if not args.disable_metadata:
            metadata = {"prompt": prompt_info}
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata[x] = dumps(extra_pnginfo[x])
        filename = f"{filename}_{counter:05}_.latent"

        results = list()
        results.append({"filename": filename, "subfolder": subfolder, "type": "output"})

        save_torch_file(
            {
                "latent_tensor": samples["samples"],
                "latent_format_version_0": torch.tensor([]),
            },
            path.join(full_output_folder, filename),
            metadata=metadata,
        )

        return {"ui": {"latents": results}}
