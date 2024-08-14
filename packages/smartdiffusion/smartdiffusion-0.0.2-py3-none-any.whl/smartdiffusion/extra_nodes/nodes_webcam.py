from smartdiffusion.config import MAX_RESOLUTION
from smartdiffusion import folder_paths


class WebcamCapture(config.LoadImage):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("WEBCAM", {}),
                "width": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1},
                ),
                "height": (
                    "INT",
                    {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1},
                ),
                "capture_on_queue": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_capture"

    CATEGORY = "image"

    def load_capture(s, image, **kwargs):
        return super().load_image(folder_paths.get_annotated_filepath(image))


NODE_CLASS_MAPPINGS = {
    "WebcamCapture": WebcamCapture,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebcamCapture": "Webcam Capture",
}
