"""
check_submission.py -- grade your Sonic Co-Performer agent on the PUBLIC data
=============================================================================

Runs the same checks the autograder runs, on the public dataset shipped in
``data/``, and prints the 80-point automated breakdown so you can see where you
stand before submitting.

    python check_submission.py                       # grades ./submission.py
    python check_submission.py --submission mine.py

What it measures (identical rubric to the real grader):

    setup / API        3   all six functions present and callable
    cue classification 25   macro-F1 over the six cues
    policy            25   action accuracy (<=18) + drift-repair rate (<=7)
    synthesis         12   a valid waveform for each of the six actions
    runtime            8   wall-clock of your code (data loading excluded)
    memory             7   peak traced memory

IMPORTANT -- this is a *practice* harness, not your grade:
  * It uses the public dataset in ``data/``. Your official grade is computed on
    a separate, unseen dataset of the same kind, so a high score here means your
    approach generalizes, not that you have memorized these files.
  * Runtime and memory depend on your machine; the points use the same
    thresholds as the grader but exact seconds/MB will vary.

This file does NOT contain the dataset generator -- it only loads and scores.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
import tracemalloc
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

import sonic_data

CUES = sonic_data.CUES
ACTIONS = sonic_data.ACTIONS
SR = sonic_data.SR
REQUIRED_FUNCTIONS = ("extract_features", "fit_cue_model", "predict_cue",
                      "reset_policy", "choose_action", "synthesize_response")

MAX_POINTS = {"setup": 3, "cue": 25, "policy": 25, "synthesis": 12,
              "runtime": 8, "memory": 7, "autograded_total": 80}


# --------------------------------------------------------------------------- #
# Submission loading + metric helpers (same contract as the autograder)
# --------------------------------------------------------------------------- #

def load_submission(path: Path) -> Tuple[Optional[Any], Optional[str]]:
    path = Path(path).resolve()
    if not path.exists():
        return None, f"submission file not found: {path}"
    mod_name = f"submission_{uuid.uuid4().hex}"
    try:
        spec = importlib.util.spec_from_file_location(mod_name, str(path))
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
        return module, None
    except Exception:
        return None, f"import failed:\n{traceback.format_exc()}"


def api_ok(module) -> Tuple[bool, List[str]]:
    missing = [n for n in REQUIRED_FUNCTIONS if not callable(getattr(module, n, None))]
    return (not missing), missing


def macro_f1(y_true: List[str], y_pred: List[str], labels: List[str]) -> float:
    try:
        from sklearn.metrics import f1_score
        return float(f1_score(y_true, y_pred, labels=labels,
                              average="macro", zero_division=0))
    except Exception:
        scores = []
        for lab in labels:
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == lab and p == lab)
            fp = sum(1 for t, p in zip(y_true, y_pred) if t != lab and p == lab)
            fn = sum(1 for t, p in zip(y_true, y_pred) if t == lab and p != lab)
            prec = tp / (tp + fp) if (tp + fp) else 0.0
            rec = tp / (tp + fn) if (tp + fn) else 0.0
            scores.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0.0)
        return float(np.mean(scores)) if scores else 0.0


def validate_waveform(w: Any, sr: int, duration: float) -> bool:
    try:
        arr = np.asarray(w, dtype=np.float64)
    except Exception:
        return False
    if arr.ndim != 1 or arr.size == 0 or not np.all(np.isfinite(arr)):
        return False
    expected = sr * duration
    if not (0.8 * expected <= arr.size <= 1.2 * expected):
        return False
    max_abs = float(np.max(np.abs(arr)))
    if max_abs > 10.0:
        return False
    normalized = arr / max_abs if max_abs > 0 else arr
    return bool(np.all(np.abs(normalized) <= 1.0 + 1e-6))


# Point brackets -- copied verbatim from the grading contract.
def points_cue(f1: float) -> int:
    for thr, pts in [(0.92, 25), (0.86, 22), (0.78, 18), (0.65, 13), (0.50, 8)]:
        if f1 >= thr:
            return pts
    return 0


def points_policy_accuracy(acc: float) -> int:
    for thr, pts in [(0.95, 18), (0.90, 16), (0.80, 13), (0.65, 8), (0.50, 4)]:
        if acc >= thr:
            return pts
    return 0


def points_drift(rate: float) -> int:
    if rate >= 1.0:
        return 7
    for thr, pts in [(0.90, 6), (0.75, 4), (0.50, 2)]:
        if rate >= thr:
            return pts
    return 0


def points_runtime(elapsed: float) -> int:
    if elapsed <= 20:
        return 8
    if elapsed <= 45:
        return 6
    if elapsed <= 90:
        return 3
    return 0


def points_memory(mb: float) -> int:
    if mb <= 1024:
        return 7
    if mb <= 2048:
        return 5
    if mb <= 4096:
        return 3
    return 0


# --------------------------------------------------------------------------- #
# The exercise (same order of operations the grader uses)
# --------------------------------------------------------------------------- #

def _exercise(module, train, test, sequences, sr: int):
    model = module.fit_cue_model(train)

    y_true: List[str] = []
    y_pred: List[str] = []
    for it in test:
        y_true.append(it["cue"])
        y_pred.append(str(module.predict_cue(model, it["audio"], it["sr"])))

    total = correct = drift_total = drift_ok = 0
    for seq in sequences:
        state = module.reset_policy()
        for step in seq:
            action, state = module.choose_action(step["cue"], step["features"], state)
            action = str(action)
            total += 1
            correct += int(action == step["target_action"])
            if step["cue"] == "drift":
                drift_total += 1
                drift_ok += int(action == "repair_topic")

    synth_valid: Dict[str, bool] = {}
    for action in ACTIONS:
        try:
            synth_valid[action] = validate_waveform(
                module.synthesize_response(action, 0, sr, 1.0), sr, 1.0)
        except Exception:
            synth_valid[action] = False

    return y_true, y_pred, {
        "total": total, "correct": correct,
        "drift_total": drift_total, "drift_ok": drift_ok}, synth_valid


def grade(submission_path: Path) -> Dict[str, Any]:
    module, err = load_submission(submission_path)
    if err:
        return {"error": err, "points": {k: 0 for k in MAX_POINTS}}

    ok, missing = api_ok(module)
    if not ok:
        return {"error": f"missing/uncallable functions: {missing}",
                "points": {k: 0 for k in MAX_POINTS}}

    # Load once (excluded from the timed region, like the grader).
    train = sonic_data.load_split("train")
    test = sonic_data.load_split("test")
    sequences = sonic_data.load_sequences()

    # Pass 1 -- clean wall clock over the student code only.
    t0 = time.perf_counter()
    y_true, y_pred, counts, synth_valid = _exercise(module, train, test, sequences, SR)
    elapsed = time.perf_counter() - t0

    # Pass 2 -- realistic memory (load + exercise) under tracemalloc.
    tracemalloc.start()
    m_train = sonic_data.load_split("train")
    m_test = sonic_data.load_split("test")
    m_seq = sonic_data.load_sequences()
    _exercise(module, m_train, m_test, m_seq, SR)
    peak_mb = tracemalloc.get_traced_memory()[1] / (1024 * 1024)
    tracemalloc.stop()

    total = counts["total"]
    drift_total = counts["drift_total"]
    f1 = macro_f1(y_true, y_pred, list(CUES))
    cue_acc = float(np.mean([a == b for a, b in zip(y_pred, y_true)])) if y_true else 0.0
    policy_acc = counts["correct"] / total if total else 0.0
    drift_rate = counts["drift_ok"] / drift_total if drift_total else 0.0
    n_valid = int(sum(synth_valid.values()))

    acc_pts = points_policy_accuracy(policy_acc)
    drift_pts = points_drift(drift_rate)
    points = {
        "setup": 3,
        "cue": points_cue(f1),
        "policy_accuracy_points": acc_pts,
        "drift_points": drift_pts,
        "policy": acc_pts + drift_pts,
        "synthesis": 2 * n_valid,
        "runtime": points_runtime(elapsed),
        "memory": points_memory(peak_mb),
    }
    points["autograded_total"] = (
        points["setup"] + points["cue"] + points["policy"]
        + points["synthesis"] + points["runtime"] + points["memory"])

    return {
        "error": None,
        "metrics": {
            "macro_f1": f1, "cue_accuracy": cue_acc,
            "policy_accuracy": policy_acc, "drift_repair_rate": drift_rate,
            "n_synthesis_valid": n_valid, "synthesis_valid": synth_valid,
            "elapsed_seconds": elapsed, "peak_memory_mb": peak_mb,
            "n_train": len(train), "n_test": len(test),
            "n_policy_steps": total, "n_drift_steps": drift_total,
        },
        "points": points,
    }


def print_report(result: Dict[str, Any]) -> None:
    print("=" * 62)
    print("  Sonic Co-Performer -- public self-check")
    print("-" * 62)
    if result.get("error"):
        print("  Could not grade your submission:")
        for line in str(result["error"]).splitlines():
            print(f"    {line}")
        print("=" * 62)
        return
    m = result["metrics"]
    p = result["points"]
    print(f"  macro-F1 (cue)     : {m['macro_f1']:.4f}   over {m['n_test']} dev items")
    print(f"  policy accuracy    : {m['policy_accuracy']:.4f}   over {m['n_policy_steps']} steps")
    print(f"  drift repair rate  : {m['drift_repair_rate']:.4f}   over {m['n_drift_steps']} drift steps")
    print(f"  synthesis valid    : {m['n_synthesis_valid']}/6")
    print(f"  elapsed seconds    : {m['elapsed_seconds']:.2f}")
    print(f"  peak memory (MB)   : {m['peak_memory_mb']:.1f}")
    print("-" * 62)
    print(f"  setup     {p['setup']:>3} / 3")
    print(f"  cue       {p['cue']:>3} / 25")
    print(f"  policy    {p['policy']:>3} / 25   "
          f"(accuracy {p['policy_accuracy_points']} + drift {p['drift_points']})")
    print(f"  synthesis {p['synthesis']:>3} / 12")
    print(f"  runtime   {p['runtime']:>3} / 8")
    print(f"  memory    {p['memory']:>3} / 7")
    print("=" * 62)
    print(f"  AUTOMATED TOTAL : {p['autograded_total']} / 80   (+20 manual report)")
    print("  Reminder: your real grade uses a separate unseen dataset.")
    print("=" * 62)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Grade your submission on public data.")
    ap.add_argument("--submission", default="submission.py",
                    help="path to your submission.py (default: ./submission.py)")
    args = ap.parse_args(argv)
    print_report(grade(Path(args.submission)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
