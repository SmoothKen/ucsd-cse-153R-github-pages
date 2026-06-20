# Sonic Co-Performer Agent — Student Release

You are building a small **musical duet agent**. A human co-performer plays
short audio "cues"; your agent must **listen** (classify the cue), **decide**
(choose an action), and **respond** (synthesize a short sound).

## The six cues and their correct actions

| Cue | Sounds like | Correct action |
|-----|-------------|----------------|
| `call` | a rising phrase, an invitation | `mirror_topic` |
| `answer` | a falling phrase, a reply | `complement_topic` |
| `hold` | near-silence, a held breath | `wait` |
| `interrupt` | percussive, bursty overlap | `yield_repair` |
| `drift` | a **loud, off-topic** lure | `repair_topic` |
| `end` | a decaying final cadence | `close` |

The tricky one is **`drift`**: it is the loudest, most attention-grabbing cue,
and a naive agent will be tempted to mirror it. The musically correct move is to
*repair* — steer back to the shared topic. Drift handling is worth dedicated
points, and it is up to your classifier to recognize a drift from the audio.

## What you submit

A single file, **`submission.py`**, implementing exactly these six functions
(do **not** rename them or change their signatures):

```python
extract_features(audio, sr) -> np.ndarray
fit_cue_model(train_items) -> model
predict_cue(model, audio, sr) -> str          # one of the six cue labels
reset_policy() -> dict
choose_action(cue, features, state) -> (action, new_state)
synthesize_response(action, topic_id, sr=16000, duration=1.0) -> np.ndarray
```

The provided `submission.py` already runs and earns the synthesis / runtime /
memory points, but ships a majority-class classifier and a `wait`-everything
policy. Your job is to fill in the two `TODO`s: a **real cue classifier** (the
heart of the assignment) and the correct **cue → action** policy.

## What you're given

```
submission.py        <- the only file you edit and submit
check_submission.py  <- run this to score yourself on the public data
sonic_data.py        <- helper to load the provided audio + labels
requirements.txt
data/
  labels.csv         <- cue / topic / action label for every clip
  sequences.json     <- scripted duet sequences for the policy
  train/  (360 wavs) <- labelled training audio (6 cues x 60)
  test/   (240 wavs) <- labelled audio to use as your dev/validation set
```

The audio is real 16 kHz mono WAVs. **Listen to them and measure them** — that
is how you discover what separates the cues (energy, spectral shape, frequency
motion, onset density, decay). There is deliberately no list of "the right
features"; finding them is the assignment.

Load the data in your code with the provided helper:

```python
from sonic_data import load_split
train = load_split("train")          # list of labelled item dicts
model = fit_cue_model(train)         # your function
```

Each item is a dict with keys `audio` (1-D float64 in [-1, 1]), `sr` (16000),
`cue`, `topic_id`, `target_action`, and `item_id`.

## Setup

```bash
python -m venv .venv
# Windows:        .venv\Scripts\Activate.ps1
# macOS / Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

Allowed dependencies only: **numpy, scipy, scikit-learn, joblib**. CPU only —
no GPU, no internet, no extra packages.

## Check your work

```bash
python check_submission.py                       # scores ./submission.py
python check_submission.py --submission mine.py
```

This prints an 80-point breakdown using the **public practice** dataset in
`data/`. It does not generate any audio — it loads exactly the files you were
given and applies the same rubric as the real grader.

Your official grade is computed on a **separate, unseen** dataset of the same
kind (you do not have it), plus **20 manual points** for your written report. An
approach that genuinely learns the cues scores the same on the public data and
the hidden set; one that overfits these particular files will not — so treat
`test/` as a held-out check, not a target.

## Grading at a glance (80 automated + 20 report)

| Component | Points | How to earn it |
|-----------|-------:|----------------|
| Setup / API | 3 | all six functions present with correct signatures |
| Cue classification | 25 | macro-F1 ≥ 0.92 for full marks |
| Policy | 25 | action accuracy (≤18) + drift repair (≤7) |
| Synthesis | 12 | 2 per action that returns a valid waveform |
| Runtime | 8 | full run ≤ 20 s |
| Memory | 7 | peak ≤ 1 GB |
| **Report** | **20** | features, classifier, policy, failure analysis, improv connection (with a citation) |

Good luck, and listen closely.
