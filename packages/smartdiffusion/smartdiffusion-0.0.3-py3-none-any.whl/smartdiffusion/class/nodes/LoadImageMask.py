import os
import hashlib
from PIL import Image, ImageOps
from numpy import array, float32
from smartdiffusion.folder_paths import (
    get_input_directory,
    get_annotated_filepath,
    exists_annotated_filepath,
)
from smartdiffusion.node_helpers import pillow


class LoadImageMask:
    _color_channels = ["alpha", "red", "green", "blue"]

    @classmethod
    def INPUT_TYPES(s):
        input_dir = get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
                "channel": (s._color_channels,),
            }
        }

    CATEGORY = "mask"

    RETURN_TYPES = ("MASK",)
    FUNCTION = "load_image"

    def load_image(self, image, channel):
        image_path = get_annotated_filepath(image)
        i = pillow(Image.open, image_path)
        i = pillow(ImageOps.exif_transpose, i)
        if i.getbands() != ("R", "G", "B", "A"):
            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            i = i.convert("RGBA")
        mask = None
        c = channel[0].upper()
        if c in i.getbands():
            mask = array(i.getchannel(c)).astype(float32) / 255.0
            mask = torch.from_numpy(mask)
            if c == "A":
                mask = 1.0 - mask
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
        return (mask.unsqueeze(0),)

    @classmethod
    def IS_CHANGED(s, image, channel):
        image_path = get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True
