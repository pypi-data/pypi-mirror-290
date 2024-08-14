from torch import tensor
from smartdiffusion.sd import VAE
from smartdiffusion.utils import load_torch_file
from smartdiffusion.folder_paths import get_filename_list, get_full_path


class VAELoader:
    @staticmethod
    def vae_list():
        vaes = get_filename_list("vae")
        approx_vaes = get_filename_list("vae_approx")
        sdxl_taesd_enc = False
        sdxl_taesd_dec = False
        sd1_taesd_enc = False
        sd1_taesd_dec = False
        sd3_taesd_enc = False
        sd3_taesd_dec = False

        for v in approx_vaes:
            if v.startswith("taesd_decoder."):
                sd1_taesd_dec = True
            elif v.startswith("taesd_encoder."):
                sd1_taesd_enc = True
            elif v.startswith("taesdxl_decoder."):
                sdxl_taesd_dec = True
            elif v.startswith("taesdxl_encoder."):
                sdxl_taesd_enc = True
            elif v.startswith("taesd3_decoder."):
                sd3_taesd_dec = True
            elif v.startswith("taesd3_encoder."):
                sd3_taesd_enc = True
        if sd1_taesd_dec and sd1_taesd_enc:
            vaes.append("taesd")
        if sdxl_taesd_dec and sdxl_taesd_enc:
            vaes.append("taesdxl")
        if sd3_taesd_dec and sd3_taesd_enc:
            vaes.append("taesd3")
        return vaes

    @staticmethod
    def load_taesd(name):
        taesd = {}
        approx_vaes = get_filename_list("vae_approx")
        enc = load_torch_file(
            get_full_path(
                "vae_approx",
                next(
                    filter(
                        lambda a: a.startswith("{}_encoder.".format(name)), approx_vaes
                    )
                ),
            )
        )
        for k in enc:
            taesd["taesd_encoder.{}".format(k)] = enc[k]
        dec = load_torch_file(
            get_full_path(
                "vae_approx",
                next(
                    filter(
                        lambda a: a.startswith("{}_decoder.".format(name)), approx_vaes
                    )
                ),
            )
        )
        for k in dec:
            taesd["taesd_decoder.{}".format(k)] = dec[k]
        if name == "taesd":
            taesd["vae_scale"] = tensor(0.18215)
            taesd["vae_shift"] = tensor(0.0)
        elif name == "taesdxl":
            taesd["vae_scale"] = tensor(0.13025)
            taesd["vae_shift"] = tensor(0.0)
        elif name == "taesd3":
            taesd["vae_scale"] = tensor(1.5305)
            taesd["vae_shift"] = tensor(0.0609)
        return taesd

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"vae_name": (s.vae_list(),)}}

    RETURN_TYPES = ("VAE",)
    FUNCTION = "load_vae"

    CATEGORY = "loaders"

    # TODO: scale factor?

    def load_vae(self, vae_name):
        if vae_name in ["taesd", "taesdxl", "taesd3"]:
            vae = self.load_taesd(vae_name)
        else:
            vae = load_torch_file(get_full_path("vae", vae_name))
        return (VAE(sd=vae),)
