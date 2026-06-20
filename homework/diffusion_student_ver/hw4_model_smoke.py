#!/usr/bin/env python3
"""Model-load smoke test for the CSE153 HW4 diffusion assignment.

Run this only after hw4_preflight.py passes. It downloads and loads the
Stable Audio model, so it can take time and disk space.
"""

from __future__ import annotations

import os
import time


def main() -> int:
    if not (os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")):
        print("FAIL no HF_TOKEN or HUGGINGFACE_HUB_TOKEN visible")
        return 1

    start = time.time()
    print("Loading stabilityai/stable-audio-open-1.0...")

    import torch
    from stable_audio_tools import get_pretrained_model

    model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
    elapsed = time.time() - start

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    print("OK model loaded")
    print(f"device={device}")
    print(f"sample_rate={model_config.get('sample_rate')}")
    print(f"sample_size={model_config.get('sample_size')}")
    print(f"elapsed_seconds={elapsed:.1f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
