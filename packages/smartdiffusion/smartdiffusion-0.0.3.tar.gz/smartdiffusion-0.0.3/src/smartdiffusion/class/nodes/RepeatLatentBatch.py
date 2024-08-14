from math import ceil


class RepeatLatentBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "amount": ("INT", {"default": 1, "min": 1, "max": 64}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "repeat"

    CATEGORY = "latent/batch"

    def repeat(self, samples, amount):
        s = samples.copy()
        s_in = samples["samples"]

        s["samples"] = s_in.repeat((amount, 1, 1, 1))
        if "noise_mask" in samples and samples["noise_mask"].shape[0] > 1:
            masks = samples["noise_mask"]
            if masks.shape[0] < s_in.shape[0]:
                masks = masks.repeat(ceil(s_in.shape[0] / masks.shape[0]), 1, 1, 1)[
                    : s_in.shape[0]
                ]
            s["noise_mask"] = samples["noise_mask"].repeat((amount, 1, 1, 1))
        if "batch_index" in s:
            offset = max(s["batch_index"]) - min(s["batch_index"]) + 1
            s["batch_index"] = s["batch_index"] + [
                x + (i * offset) for i in range(1, amount) for x in s["batch_index"]
            ]
        return (s,)
