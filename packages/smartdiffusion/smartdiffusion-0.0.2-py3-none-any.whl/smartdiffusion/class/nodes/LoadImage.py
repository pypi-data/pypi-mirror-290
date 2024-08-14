from torch import from_numpy, zeros, float32, cat
from os import path, listdir
from hashlib import sha256
from PIL import Image, ImageOps, ImageSequence
from numpy import array, float32
from smartdiffusion.folder_paths import (
    get_input_directory,
    get_annotated_filepath,
    exists_annotated_filepath,
)
from smartdiffusion.node_helpers import pillow


class LoadImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = get_input_directory()
        files = [f for f in listdir(input_dir) if path.isfile(path.join(input_dir, f))]
        return {
            "required": {"image": (sorted(files), {"image_upload": True})},
        }

    CATEGORY = "image"

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = get_annotated_filepath(image)

        img = pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ["MPO"]

        for i in ImageSequence.Iterator(img):
            i = pillow(ImageOps.exif_transpose, i)

            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]
            if image.size[0] != w or image.size[1] != h:
                continue
            image = array(image).astype(float32) / 255.0
            image = from_numpy(image)[None,]
            if "A" in i.getbands():
                mask = array(i.getchannel("A")).astype(float32) / 255.0
                mask = 1.0 - from_numpy(mask)
            else:
                mask = zeros((64, 64), dtype=float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))
        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = cat(output_images, dim=0)
            output_mask = cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]
        return (output_image, output_mask)

    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_annotated_filepath(image)
        m = sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True
