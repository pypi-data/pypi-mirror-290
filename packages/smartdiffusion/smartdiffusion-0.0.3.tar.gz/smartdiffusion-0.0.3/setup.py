#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

setup(
    name = "smartdiffusion",
    version = "0.0.3",
    description = "A library for making it easier to work with neural networks",
    long_description = "A library for making it easier to work with neural networks",
    url ="https://github.com/jslegers/smartdiffusion",
    author ="John Slegers",
    license = "GNU v3",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    python_requires=">=3.8.0",
    install_requires = [
        "torch",
        "torchsde",
        "torchvision",
        "torchaudio",
        "einops",
        "transformers>=4.28.1",
        "tokenizers>=0.13.3",
        "sentencepiece",
        "safetensors>=0.4.2",
        "pyyaml",
        "Pillow",
        "scipy",
        "tqdm",
        "psutil",
        "accelerate",
        "huggingface_hub",
        "xformers>=0.0.27"
    ]
)
