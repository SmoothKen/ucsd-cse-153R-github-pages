"""
sonic_data.py -- load the provided Sonic Co-Performer dataset
=============================================================

A tiny, dependency-light loader for the audio + labels shipped in ``data/``.
It turns the WAV files and ``labels.csv`` back into the same item dictionaries
the grader uses, and loads the interaction sequences for policy testing.

There is **no synthesis here** -- this only *reads* what is on disk. Discovering
what makes each cue sound different is your job (that is the assignment); listen
to the WAVs and measure them.

Item dictionaries have exactly the keys the grader expects::

    {
      "audio":         np.ndarray,   # 1-D float64 in [-1, 1], 16 kHz
      "sr":            16000,
      "cue":           "call" | "answer" | "hold" | "interrupt" | "drift" | "end",
      "topic_id":      int,
      "target_action": str,          # the correct action for this cue
      "item_id":       str,
    }

Typical use in ``submission.py`` development::

    from sonic_data import load_split
    train = load_split("train")          # list of item dicts (labelled)
    model = fit_cue_model(train)         # your function

Splits:
    "train"  -- 6 cues x 60 = 360 labelled items to train on.
    "test"   -- 6 cues x 40 = 240 items; use as your local dev/validation set.

Your real grade is computed on a separate, unseen dataset, so do not overfit to
these particular files -- treat ``test`` as a held-out check, not a target.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from scipy.io import wavfile

DATA_DIR = Path(__file__).resolve().parent / "data"
SR = 16000
CUES = ("call", "answer", "hold", "interrupt", "drift", "end")
ACTIONS = ("mirror_topic", "complement_topic", "wait",
           "yield_repair", "repair_topic", "close")


def _read_wav(path: Path) -> np.ndarray:
    """Read a 16-bit PCM WAV into a 1-D float64 array in [-1, 1]."""
    sr, data = wavfile.read(str(path))
    x = np.asarray(data)
    if x.ndim > 1:                       # collapse to mono if ever stereo
        x = x.mean(axis=1)
    if np.issubdtype(x.dtype, np.integer):
        x = x.astype(np.float64) / 32768.0
    else:
        x = x.astype(np.float64)
    return x


def _read_labels() -> List[Dict[str, str]]:
    labels_path = DATA_DIR / "labels.csv"
    if not labels_path.exists():
        raise FileNotFoundError(
            f"labels.csv not found at {labels_path}. Run from the release root "
            f"so that ./data/ is alongside this file.")
    with labels_path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def load_split(split: str) -> List[Dict[str, Any]]:
    """Load all items for ``split`` ("train" or "test") as item dictionaries."""
    rows = [r for r in _read_labels() if r["split"] == split]
    if not rows:
        raise ValueError(f"no items found for split {split!r} in labels.csv")
    items: List[Dict[str, Any]] = []
    for r in rows:
        audio = _read_wav(DATA_DIR / r["path"])
        items.append({
            "audio": audio,
            "sr": SR,
            "cue": r["cue"],
            "topic_id": int(r["topic_id"]),
            "target_action": r["target_action"],
            "item_id": r["item_id"],
        })
    return items


def load_sequences() -> List[List[Dict[str, Any]]]:
    """Load the interaction sequences for policy evaluation.

    Each step is ``{cue, topic_id, target_action, features}`` with ``features``
    as a 1-D float64 array (your policy receives it but may ignore it).
    """
    seq_path = DATA_DIR / "sequences.json"
    if not seq_path.exists():
        raise FileNotFoundError(f"sequences.json not found at {seq_path}.")
    raw = json.loads(seq_path.read_text())
    sequences: List[List[Dict[str, Any]]] = []
    for seq in raw:
        steps = []
        for step in seq:
            steps.append({
                "cue": step["cue"],
                "topic_id": int(step["topic_id"]),
                "target_action": step["target_action"],
                "features": np.asarray(step["features"], dtype=np.float64),
            })
        sequences.append(steps)
    return sequences


if __name__ == "__main__":  # quick peek at what is available
    tr = load_split("train")
    te = load_split("test")
    seqs = load_sequences()
    print(f"train items : {len(tr)}")
    print(f"dev items   : {len(te)}")
    print(f"sequences   : {len(seqs)} "
          f"({sum(len(s) for s in seqs)} steps, "
          f"{sum(1 for s in seqs for st in s if st['cue'] == 'drift')} drift)")
    for c in CUES:
        ex = next(it for it in tr if it["cue"] == c)
        a = ex["audio"]
        print(f"  {c:9s} -> {ex['target_action']:16s} "
              f"len={len(a):6d} rms={np.sqrt(np.mean(a**2)):.4f} "
              f"peak={np.max(np.abs(a)):.4f}")
