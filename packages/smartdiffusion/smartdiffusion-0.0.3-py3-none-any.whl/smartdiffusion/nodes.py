# sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "smartdiffusion"))


from smartdiffusion import model_management
from smartdiffusion.load import module


def before_node_execution():
    model_management.throw_exception_if_processing_interrupted()


def interrupt_processing(value=True):
    model_management.interrupt_current_processing(value)


NODE_CLASS_MAPPINGS = {
    "KSampler": module("smartdiffusion", "KSampler"),
    "CheckpointLoaderSimple": module("smartdiffusion", "CheckpointLoaderSimple"),
    "CLIPTextEncode": module("smartdiffusion", "CLIPTextEncode"),
    "CLIPSetLastLayer": module("smartdiffusion", "CLIPSetLastLayer"),
    "VAEDecode": module("smartdiffusion", "VAEDecode"),
    "VAEEncode": module("smartdiffusion", "VAEEncode"),
    "VAEEncodeForInpaint": module("smartdiffusion", "VAEEncodeForInpaint"),
    "VAELoader": module("smartdiffusion", "VAELoader"),
    "EmptyLatentImage": module("smartdiffusion", "EmptyLatentImage"),
    "LatentUpscale": module("smartdiffusion", "LatentUpscale"),
    "LatentUpscaleBy": module("smartdiffusion", "LatentUpscaleBy"),
    "LatentFromBatch": module("smartdiffusion", "LatentFromBatch"),
    "RepeatLatentBatch": module("smartdiffusion", "RepeatLatentBatch"),
    "SaveImage": module("smartdiffusion", "SaveImage"),
    "PreviewImage": module("smartdiffusion", "PreviewImage"),
    "LoadImage": module("smartdiffusion", "LoadImage"),
    "LoadImageMask": module("smartdiffusion", "LoadImageMask"),
    "ImageScale": module("smartdiffusion", "ImageScale"),
    "ImageScaleBy": module("smartdiffusion", "ImageScaleBy"),
    "ImageInvert": module("smartdiffusion", "ImageInvert"),
    "ImageBatch": module("smartdiffusion", "ImageBatch"),
    "ImagePadForOutpaint": module("smartdiffusion", "ImagePadForOutpaint"),
    "EmptyImage": module("smartdiffusion", "EmptyImage"),
    "ConditioningAverage": module("smartdiffusion", "ConditioningAverage"),
    "ConditioningCombine": module("smartdiffusion", "ConditioningCombine"),
    "ConditioningConcat": module("smartdiffusion", "ConditioningConcat"),
    "ConditioningSetArea": module("smartdiffusion", "ConditioningSetArea"),
    "ConditioningSetAreaPercentage": module(
        "smartdiffusion", "ConditioningSetAreaPercentage"
    ),
    "ConditioningSetAreaStrength": module(
        "smartdiffusion", "ConditioningSetAreaStrength"
    ),
    "ConditioningSetMask": module("smartdiffusion", "ConditioningSetMask"),
    "KSamplerAdvanced": module("smartdiffusion", "KSamplerAdvanced"),
    "SetLatentNoiseMask": module("smartdiffusion", "SetLatentNoiseMask"),
    "LatentComposite": module("smartdiffusion", "LatentComposite"),
    "LatentBlend": module("smartdiffusion", "LatentBlend"),
    "LatentRotate": module("smartdiffusion", "LatentRotate"),
    "LatentFlip": module("smartdiffusion", "LatentFlip"),
    "LatentCrop": module("smartdiffusion", "LatentCrop"),
    "LoraLoader": module("smartdiffusion", "LoraLoader"),
    "CLIPLoader": module("smartdiffusion", "CLIPLoader"),
    "UNETLoader": module("smartdiffusion", "UNETLoader"),
    "DualCLIPLoader": module("smartdiffusion", "DualCLIPLoader"),
    "CLIPVisionEncode": module("smartdiffusion", "CLIPVisionEncode"),
    "StyleModelApply": module("smartdiffusion", "StyleModelApply"),
    "unCLIPConditioning": module("smartdiffusion", "unCLIPConditioning"),
    "ControlNetApply": module("smartdiffusion", "ControlNetApply"),
    "ControlNetApplyAdvanced": module("smartdiffusion", "ControlNetApplyAdvanced"),
    "ControlNetLoader": module("smartdiffusion", "ControlNetLoader"),
    "DiffControlNetLoader": module("smartdiffusion", "DiffControlNetLoader"),
    "StyleModelLoader": module("smartdiffusion", "StyleModelLoader"),
    "CLIPVisionLoader": module("smartdiffusion", "CLIPVisionLoader"),
    "VAEDecodeTiled": module("smartdiffusion", "VAEDecodeTiled"),
    "VAEEncodeTiled": module("smartdiffusion", "VAEEncodeTiled"),
    "unCLIPCheckpointLoader": module("smartdiffusion", "unCLIPCheckpointLoader"),
    "GLIGENLoader": module("smartdiffusion", "GLIGENLoader"),
    "GLIGENTextBoxApply": module("smartdiffusion", "GLIGENTextBoxApply"),
    "InpaintModelConditioning": module("smartdiffusion", "InpaintModelConditioning"),
    "CheckpointLoader": module("smartdiffusion", "CheckpointLoader"),
    "DiffusersLoader": module("smartdiffusion", "DiffusersLoader"),
    "LoadLatent": module("smartdiffusion", "LoadLatent"),
    "SaveLatent": module("smartdiffusion", "SaveLatent"),
    "ConditioningZeroOut": module("smartdiffusion", "ConditioningZeroOut"),
    "ConditioningSetTimestepRange": module(
        "smartdiffusion", "ConditioningSetTimestepRange"
    ),
    "LoraLoaderModelOnly": module("smartdiffusion", "LoraLoaderModelOnly"),
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Sampling
    "KSampler": "KSampler",
    "KSamplerAdvanced": "KSampler (Advanced)",
    # Loaders
    "CheckpointLoader": "Load Checkpoint With Config (DEPRECATED)",
    "CheckpointLoaderSimple": "Load Checkpoint",
    "VAELoader": "Load VAE",
    "LoraLoader": "Load LoRA",
    "CLIPLoader": "Load CLIP",
    "ControlNetLoader": "Load ControlNet Model",
    "DiffControlNetLoader": "Load ControlNet Model (diff)",
    "StyleModelLoader": "Load Style Model",
    "CLIPVisionLoader": "Load CLIP Vision",
    "UpscaleModelLoader": "Load Upscale Model",
    "UNETLoader": "Load Diffusion Model",
    # Conditioning
    "CLIPVisionEncode": "CLIP Vision Encode",
    "StyleModelApply": "Apply Style Model",
    "CLIPTextEncode": "CLIP Text Encode (Prompt)",
    "CLIPSetLastLayer": "CLIP Set Last Layer",
    "ConditioningCombine": "Conditioning (Combine)",
    "ConditioningAverage ": "Conditioning (Average)",
    "ConditioningConcat": "Conditioning (Concat)",
    "ConditioningSetArea": "Conditioning (Set Area)",
    "ConditioningSetAreaPercentage": "Conditioning (Set Area with Percentage)",
    "ConditioningSetMask": "Conditioning (Set Mask)",
    "ControlNetApply": "Apply ControlNet",
    "ControlNetApplyAdvanced": "Apply ControlNet (Advanced)",
    # Latent
    "VAEEncodeForInpaint": "VAE Encode (for Inpainting)",
    "SetLatentNoiseMask": "Set Latent Noise Mask",
    "VAEDecode": "VAE Decode",
    "VAEEncode": "VAE Encode",
    "LatentRotate": "Rotate Latent",
    "LatentFlip": "Flip Latent",
    "LatentCrop": "Crop Latent",
    "EmptyLatentImage": "Empty Latent Image",
    "LatentUpscale": "Upscale Latent",
    "LatentUpscaleBy": "Upscale Latent By",
    "LatentComposite": "Latent Composite",
    "LatentBlend": "Latent Blend",
    "LatentFromBatch": "Latent From Batch",
    "RepeatLatentBatch": "Repeat Latent Batch",
    # Image
    "SaveImage": "Save Image",
    "PreviewImage": "Preview Image",
    "LoadImage": "Load Image",
    "LoadImageMask": "Load Image (as Mask)",
    "ImageScale": "Upscale Image",
    "ImageScaleBy": "Upscale Image By",
    "ImageUpscaleWithModel": "Upscale Image (using Model)",
    "ImageInvert": "Invert Image",
    "ImagePadForOutpaint": "Pad Image for Outpainting",
    "ImageBatch": "Batch Images",
    # _for_testing
    "VAEDecodeTiled": "VAE Decode (Tiled)",
    "VAEEncodeTiled": "VAE Encode (Tiled)",
}

EXTENSION_WEB_DIRS = {}


import os


def get_module_name(module_path: str) -> str:
    """
    Returns the module name based on the given module path.
    Examples:
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node.py") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node/") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node/__init__.py") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node/__init__") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node/__init__/") -> "my_custom_node"
        get_module_name("C:/Users/username/smartdiffusionserver/custom_nodes/my_custom_node.disabled") -> "custom_nodes
    Args:
        module_path (str): The path of the module.
    Returns:
        str: The module name.
    """
    base_path = os.path.basename(module_path)
    if os.path.isfile(module_path):
        base_path = os.path.splitext(base_path)[0]
    return base_path


import os
import sys
import traceback
import logging
import importlib


def load_custom_node(
    module_path: str, ignore=set(), module_parent="custom_nodes"
) -> bool:
    module_name = os.path.basename(module_path)
    if os.path.isfile(module_path):
        sp = os.path.splitext(module_path)
        module_name = sp[0]
    try:
        logging.debug("Trying to load custom node {}".format(module_path))
        if os.path.isfile(module_path):
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_path
            )
            module_dir = os.path.split(module_path)[0]
        else:
            module_spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(module_path, "__init__.py")
            )
            module_dir = module_path
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)

        if (
            hasattr(module, "WEB_DIRECTORY")
            and getattr(module, "WEB_DIRECTORY") is not None
        ):
            web_dir = os.path.abspath(
                os.path.join(module_dir, getattr(module, "WEB_DIRECTORY"))
            )
            if os.path.isdir(web_dir):
                EXTENSION_WEB_DIRS[module_name] = web_dir
        if (
            hasattr(module, "NODE_CLASS_MAPPINGS")
            and getattr(module, "NODE_CLASS_MAPPINGS") is not None
        ):
            for name, node_cls in module.NODE_CLASS_MAPPINGS.items():
                if name not in ignore:
                    NODE_CLASS_MAPPINGS[name] = node_cls
                    node_cls.RELATIVE_PYTHON_MODULE = "{}.{}".format(
                        module_parent, get_module_name(module_path)
                    )
            if (
                hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS")
                and getattr(module, "NODE_DISPLAY_NAME_MAPPINGS") is not None
            ):
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            return True
        else:
            logging.warning(
                f"Skip {module_path} module for custom nodes due to the lack of NODE_CLASS_MAPPINGS."
            )
            return False
    except Exception as e:
        logging.warning(traceback.format_exc())
        logging.warning(f"Cannot import {module_path} module for custom nodes: {e}")
        return False


import os
import time
import logging
from smartdiffusion import folder_paths


def init_external_custom_nodes():
    """
    Initializes the external custom nodes.

    This function loads custom nodes from the specified folder paths and imports them into the application.
    It measures the import times for each custom node and logs the results.

    Returns:
        None
    """
    base_node_names = set(NODE_CLASS_MAPPINGS.keys())
    node_paths = folder_paths.get_folder_paths("custom_nodes")
    node_import_times = []
    for custom_node_path in node_paths:
        possible_modules = os.listdir(os.path.realpath(custom_node_path))
        if "__pycache__" in possible_modules:
            possible_modules.remove("__pycache__")
        for possible_module in possible_modules:
            module_path = os.path.join(custom_node_path, possible_module)
            if (
                os.path.isfile(module_path)
                and os.path.splitext(module_path)[1] != ".py"
            ):
                continue
            if module_path.endswith(".disabled"):
                continue
            time_before = time.perf_counter()
            success = load_custom_node(
                module_path, base_node_names, module_parent="custom_nodes"
            )
            node_import_times.append(
                (time.perf_counter() - time_before, module_path, success)
            )
    if len(node_import_times) > 0:
        logging.info("\nImport times for custom nodes:")
        for n in sorted(node_import_times):
            if n[2]:
                import_message = ""
            else:
                import_message = " (IMPORT FAILED)"
            logging.info("{:6.1f} seconds{}: {}".format(n[0], import_message, n[1]))
        logging.info("")


import os


def init_builtin_extra_nodes():
    """
    Initializes the built-in extra nodes in Smart Diffusion Server.

    This function loads the extra node files located in the "extra_nodes" directory and imports them into Smart Diffusion Server.
    If any of the extra node files fail to import, a warning message is logged.

    Returns:
        None
    """
    extras_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "extra_nodes"
    )
    extras_files = os.listdir(extras_dir)

    import_failed = []
    for node_file in extras_files:
        if not load_custom_node(
            os.path.join(extras_dir, node_file), module_parent="extra_nodes"
        ):
            import_failed.append(node_file)
    return import_failed


import logging
from smartdiffusion.cli_args import args


def init_extra_nodes(init_custom_nodes=True):
    import_failed = init_builtin_extra_nodes()

    if init_custom_nodes:
        init_external_custom_nodes()
    else:
        logging.info("Skipping loading of custom nodes")
    if len(import_failed) > 0:
        logging.warning(
            "WARNING: some extra_nodes/ nodes did not import correctly. This may be because they are missing some dependencies.\n"
        )
        for node in import_failed:
            logging.warning("IMPORT FAILED: {}".format(node))
        logging.warning(
            "\nThis issue might be caused by new missing dependencies added the last time you updated Smart Diffusion Server."
        )
        if args.windows_standalone_build:
            logging.warning(
                "Please run the update script: update/update_smartdiffusionserver.bat"
            )
        else:
            logging.warning("Please do a: pip install -r requirements.txt")
        logging.warning("")
