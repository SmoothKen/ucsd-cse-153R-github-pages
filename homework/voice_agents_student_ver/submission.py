"""
submission.py -- Sonic Co-Performer Agent  (STUDENT STARTER SCAFFOLD)
=====================================================================

This is the file you edit and submit. It already RUNS end to end and passes the
API, synthesis, runtime, and memory checks, but the two parts that matter --
hearing the cue and choosing the musically correct response -- are left as
clearly marked ``TODO``s. Out of the box this scaffold scores roughly 30/80:

    setup/API   3      synthesis 12      runtime 8      memory 7
    cue         0  <-- YOUR JOB (train a real classifier)
    policy      0  <-- YOUR JOB (map each cue to the right action)

Your agent listens to a short audio "cue" from a human co-performer and answers
with an action. The six cues and their musically correct actions are:

    call      -> mirror_topic        (echo the phrase back)
    answer    -> complement_topic    (respond in the same key)
    hold      -> wait                (leave space; don't step on them)
    interrupt -> yield_repair        (stop, then gracefully recover)
    drift     -> repair_topic        (they wandered off -- steer back)
    end       -> close               (land the final cadence)

The interesting one is ``drift``: it is a LOUD, attention-grabbing off-topic
lure. A naive agent mirrors whatever is loudest and gets pulled off topic; a
good agent recognizes the drift and *repairs* back to the shared theme. Getting
drift right is worth dedicated points.

Do NOT change the function names or signatures below -- the autograder calls
them exactly as written. You MAY add helper functions, features, and imports
from numpy / scipy / scikit-learn / joblib (CPU only).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np

# Canonical mappings (provided for convenience; the grader uses its own copy).
SR_DEFAULT = 16000
CUES = ("call", "answer", "hold", "interrupt", "drift", "end")
CUE_TO_ACTION = {
    "call": "mirror_topic",
    "answer": "complement_topic",
    "hold": "wait",
    "interrupt": "yield_repair",
    "drift": "repair_topic",
    "end": "close",
}
ACTIONS = tuple(CUE_TO_ACTION[c] for c in CUES)


# --------------------------------------------------------------------------- #
# 1. Feature extraction
# --------------------------------------------------------------------------- #

def extract_features(audio: np.ndarray, sr: int) -> np.ndarray:
    """Turn one cue waveform into a fixed-length feature vector.

    The scaffold ships two trivial features so the pipeline runs. To classify
    the six cues you will want features that separate them acoustically, e.g.:
      * loudness / energy           (drift is loud; hold is near-silent)
      * spectral centroid / bands   (rising vs falling vs inharmonic)
      * onset density               (interrupt is bursty/percussive)
      * pitch motion over time      (call rises; end descends)

    TODO: replace / extend these with discriminative features.
    """
    x = np.asarray(audio, dtype=np.float64).ravel()
    if x.size == 0:
        x = np.zeros(1, dtype=np.float64)
    duration_s = x.size / float(sr if sr else SR_DEFAULT)
    rms = float(np.sqrt(np.mean(x ** 2)))
    # TODO: add more features here and return a longer vector.
    return np.array([duration_s, rms], dtype=np.float64)


# --------------------------------------------------------------------------- #
# 2. Cue classifier
# --------------------------------------------------------------------------- #

def fit_cue_model(train_items: List[Dict[str, Any]]):
    """Train a model that maps a cue waveform to one of the six cue labels.

    The scaffold returns a majority-class baseline (no real learning). Replace
    this with a real classifier trained on ``extract_features`` outputs --
    a scikit-learn ``Pipeline(StandardScaler, RandomForestClassifier)`` or
    similar works well and stays within the allowed dependencies.

    TODO: extract features for every train item and fit a real classifier.
    """
    labels = [it["cue"] for it in train_items]
    # majority class (ties broken by cue order)
    counts = {c: labels.count(c) for c in CUES}
    majority = max(CUES, key=lambda c: counts[c])
    return {"model_type": "majority-baseline", "majority_class": majority,
            "classes": sorted(set(labels))}


def predict_cue(model, audio: np.ndarray, sr: int) -> str:
    """Predict the cue label for one waveform.

    TODO: run your fitted classifier on ``extract_features(audio, sr)``.
    """
    # Baseline ignores the audio entirely and always guesses the majority class.
    return str(model.get("majority_class", "hold"))


# --------------------------------------------------------------------------- #
# 3. Interaction policy
# --------------------------------------------------------------------------- #

def reset_policy() -> dict:
    """Return the agent's initial conversational state (fresh performance)."""
    return {"turn": 0, "last_action": None, "repair_count": 0}


def choose_action(cue: str, features: np.ndarray, state: dict) -> Tuple[str, dict]:
    """Given the (predicted) cue and current state, choose an action.

    The scaffold always returns ``wait`` -- which is only correct for ``hold``.
    Your job is to return the musically correct action for every cue, including
    repairing on ``drift`` rather than mirroring the loud lure.

    TODO: replace the constant ``wait`` with the correct cue -> action mapping
    and update ``state`` (e.g. advance the turn counter, track repairs).
    """
    new_state = dict(state)
    new_state["turn"] = int(state.get("turn", 0)) + 1
    action = "wait"  # TODO: map `cue` to the correct action.
    new_state["last_action"] = action
    return action, new_state


# --------------------------------------------------------------------------- #
# 4. Response synthesis
# --------------------------------------------------------------------------- #

def synthesize_response(action: str, topic_id: int, sr: int = 16000,
                        duration: float = 1.0) -> np.ndarray:
    """Render a short mono waveform for the chosen action.

    The grader only checks that the waveform is finite, mono, roughly the right
    length, and not clipping -- so this scaffold already earns synthesis points.
    Feel free to make each action sound distinct and musical.
    """
    n = max(1, int(round(duration * sr)))
    t = np.arange(n) / float(sr)
    # A different base pitch per action keeps them audibly distinct.
    base = 220.0 * (1.0 + 0.12 * (ACTIONS.index(action) if action in ACTIONS else 0))
    freq = base * (1.0 + 0.05 * (int(topic_id) % 4))
    wave = 0.2 * np.sin(2.0 * np.pi * freq * t)
    # gentle fade in/out so it is click-free
    fade = max(1, int(0.02 * sr))
    env = np.ones(n)
    env[:fade] = np.linspace(0.0, 1.0, fade)
    env[-fade:] = np.linspace(1.0, 0.0, fade)
    return (wave * env).astype(np.float64)


if __name__ == "__main__":  # tiny manual smoke test
    sr = SR_DEFAULT
    demo = np.sin(2 * np.pi * 440 * np.arange(sr) / sr).astype(np.float64)
    feats = extract_features(demo, sr)
    print("features:", feats)
    model = fit_cue_model([{"cue": c, "audio": demo, "sr": sr} for c in CUES])
    print("predict_cue:", predict_cue(model, demo, sr))
    st = reset_policy()
    for c in CUES:
        a, st = choose_action(c, feats, st)
        print(f"  {c:9s} -> {a}")
    for a in ACTIONS:
        w = synthesize_response(a, 0, sr, 1.0)
        print(f"  synth {a:16s} len={len(w)} peak={np.max(np.abs(w)):.3f}")
