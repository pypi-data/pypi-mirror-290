from math import ceil


class LatentFromBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "batch_index": ("INT", {"default": 0, "min": 0, "max": 63}),
                "length": ("INT", {"default": 1, "min": 1, "max": 64}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "frombatch"

    CATEGORY = "latent/batch"

    def frombatch(self, samples, batch_index, length):
        s = samples.copy()
        s_in = samples["samples"]
        batch_index = min(s_in.shape[0] - 1, batch_index)
        length = min(s_in.shape[0] - batch_index, length)
        s["samples"] = s_in[batch_index : batch_index + length].clone()
        if "noise_mask" in samples:
            masks = samples["noise_mask"]
            if masks.shape[0] == 1:
                s["noise_mask"] = masks.clone()
            else:
                if masks.shape[0] < s_in.shape[0]:
                    masks = masks.repeat(ceil(s_in.shape[0] / masks.shape[0]), 1, 1, 1)[
                        : s_in.shape[0]
                    ]
                s["noise_mask"] = masks[batch_index : batch_index + length].clone()
        if "batch_index" not in s:
            s["batch_index"] = [x for x in range(batch_index, batch_index + length)]
        else:
            s["batch_index"] = samples["batch_index"][
                batch_index : batch_index + length
            ]
        return (s,)
