class CLIPTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "clip": ("CLIP",),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "conditioning"

    def encode(self, clip, text):
        output = clip.encode_from_tokens(
            clip.tokenize(text), return_pooled=True, return_dict=True
        )
        cond = output.pop("cond")
        return ([[cond, output]],)
