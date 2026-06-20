#!/usr/bin/env python3
"""Preflight checks for the CSE153 HW4 diffusion notebooks.

This script intentionally does not print Hugging Face token values.
"""

from __future__ import annotations

import os
from pathlib import Path


HW4_DIR = Path(__file__).resolve().parent
REQUIRED_MODULES = [
    "torch",
    "torchaudio",
    "stable_audio_tools",
    "transformers",
    "huggingface_hub",
    "einops",
    "tqdm",
    "scipy",
    "IPython",
]


def check_imports() -> bool:
    ok = True
    print("== Package imports ==")
    for name in REQUIRED_MODULES:
        try:
            module = __import__(name)
            version = getattr(module, "__version__", "")
            print(f"OK   {name} {version}".rstrip())
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            ok = False
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    return ok


def check_hf_access() -> bool:
    from huggingface_hub import hf_hub_download

    ok = True
    print("\n== Hugging Face access ==")
    has_token = bool(os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN"))
    print(f"HF token visible: {has_token}")

    checks = [
        ("stabilityai/stable-audio-open-1.0", "model_config.json"),
        ("facebook/musicgen-small", "config.json"),
        ("facebook/musicgen-small", "preprocessor_config.json"),
    ]

    for repo, filename in checks:
        try:
            path = hf_hub_download(repo, filename=filename, repo_type="model")
            print(f"OK   {repo}/{filename}: {path}")
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            ok = False
            print(f"FAIL {repo}/{filename}: {type(exc).__name__}: {str(exc).splitlines()[0]}")
    return ok


def check_hw4_files() -> bool:
    import torch

    ok = True
    print("\n== HW4 tensor files ==")
    paths = [
        "x_T.pt",
        "testing_files/q1_0.pt",
        "testing_files/q1_1.pt",
        "testing_files/q2_0.pt",
        "testing_files/q2_1.pt",
        "testing_files/q3_0.pt",
        "testing_files/q3_1.pt",
        "testing_files/q4_0.pt",
        "testing_files/q4_1.pt",
        "testing_files/q5_0.pt",
        "testing_files/q5_1.pt",
    ]
    for rel in paths:
        path = HW4_DIR / rel
        if not path.exists():
            ok = False
            print(f"FAIL missing {rel}")
            continue
        try:
            obj = torch.load(path, map_location="cpu")
            shape = getattr(obj, "shape", None)
            dtype = getattr(obj, "dtype", None)
            print(f"OK   {rel}: {type(obj).__name__} shape={shape} dtype={dtype}")
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            ok = False
            print(f"FAIL {rel}: {type(exc).__name__}: {exc}")
    return ok


def main() -> int:
    results = [
        check_imports(),
        check_hf_access(),
        check_hw4_files(),
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
