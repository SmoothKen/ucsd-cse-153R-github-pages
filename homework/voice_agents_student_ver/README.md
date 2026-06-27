# Assignment: Sonic Co-Performer Agent

Guest module: Amir Ivry

You are building a small voice/music agent that treats sound as a control surface. A human co-performer plays short sonic cues; your agent must listen, infer the cue, choose a policy action, and synthesize a short response sound. The goal is not to train a giant audio-language model. The goal is to understand the interface between audio perception, interaction state, policy, synthesis, and behavioral evaluation.

This setting is closer to improvisation and sound poetry than to a normal chatbot. Machine musicianship asks how a system can listen to a performer and respond in a coherent style; modern audio-language models expand the input/output vocabulary, but they do not remove the need for real-time policy design, resource-aware deployment, and behavioral evaluation.

## Learning objectives

By the end of this assignment, you should be able to:

- extract interpretable acoustic features from short audio clips;
- train a lightweight cue classifier without using large pretrained models;
- implement an interaction policy that balances response, waiting, repair, and closure;
- test an agent using clear behavioral metrics rather than only audio quality;
- explain how this toy agent relates to improvisation, sound poetry, and voice-agent reliability.

## Resource constraints

This assignment is designed for UCSD DataHub-style constraints. A GPU is not required. The reference solution passes the hidden grader on CPU in roughly 9 seconds with peak traced Python memory under 150 MB. A machine without a GPU, or with a basic GPU, is sufficient.

Allowed dependencies only: **numpy, scipy, scikit-learn**. CPU only; no internet access, no model downloads, and no extra packages.

## Data: six sonic control cues

You are given labelled 16 kHz mono WAV files. Each clip has one cue label and one target policy action.

| Cue | Target action | Meaning |
|-----|---------------|---------|
| `call` | `mirror_topic` | Rising, invitation-like contour. The agent should answer in the current motif/topic. |
| `answer` | `complement_topic` | Falling response-like contour. The agent should complement the current motif. |
| `hold` | `wait` | Long silence or hesitation. The agent should not force a response. |
| `interrupt` | `yield_repair` | Burst/overlap-like cue. The agent should yield and repair timing. |
| `drift` | `repair_topic` | Salient off-topic sonic lure. The agent should not chase it; it should return to topic. |
| `end` | `close` | Decaying cadence. The agent should close the interaction. |

The key agentic idea is the **drift** case. A naive policy may imitate the most salient sound because it is loud or novel. A better co-performer notices that it is off-topic and repairs the shared context.

## What you submit

Submit a single file named **`submission.py`**. It must define exactly these six functions; do not rename them or change their signatures.

```python
def extract_features(audio: np.ndarray, sr: int) -> np.ndarray:
    ...

def fit_cue_model(train_items: list[dict]):
    ...

def predict_cue(model, audio: np.ndarray, sr: int) -> str:
    ...

def reset_policy() -> dict:
    ...

def choose_action(cue: str, features: np.ndarray, state: dict) -> tuple[str, dict]:
    ...

def synthesize_response(action: str, topic_id: int,
                        sr: int = 16000, duration: float = 1.0) -> np.ndarray:
    ...
```

The provided starter `submission.py` already runs and earns the synthesis, runtime, and memory points, but ships a majority-class classifier and a `wait`-everything policy. Your job is to implement a real cue classifier and the correct cue-to-action policy.

## What you are given

```text
submission.py        <- the only file you edit and submit
check_submission.py  <- run this to score yourself on the public data
sonic_data.py        <- helper to load the provided audio and labels
requirements.txt
data/
  labels.csv         <- cue / topic / action label for every clip
  sequences.json     <- scripted duet sequences for the policy
  train/  (360 wavs) <- labelled training audio (6 cues x 60)
  test/   (240 wavs) <- labelled audio to use as your dev/validation set
```

Load the data in your code with the provided helper:

```python
from sonic_data import load_split
train = load_split("train")
model = fit_cue_model(train)
```

Each item is a dict with keys `audio` (1-D float64 in [-1, 1]), `sr` (16000), `cue`, `topic_id`, `target_action`, and `item_id`.

Listen to the audio and measure it. Useful cues may appear in energy, zero-crossing rate, silence ratio, spectral shape, dominant-frequency motion, onset density, decay, and band-energy ratios. There is deliberately no official list of the right features; discovering them is part of the assignment.

## Part A: audio features [20 pts]

Implement `extract_features`. The feature vector must be one-dimensional, finite, and deterministic. Good features include RMS energy, peak level, zero-crossing rate, silence ratio, spectral centroid, spectral bandwidth, spectral flatness, dominant frequency, dominant-frequency motion from first half to second half, onset density, and band-energy ratios.

## Part B: cue classifier [25 pts]

Implement `fit_cue_model` and `predict_cue`. The grader supplies training items containing waveform, sampling rate, cue label, topic id, and target action. You may use a lightweight model such as logistic regression, random forest, support vector machine, or gradient boosting. The hidden score is based on macro-F1 across the six cue labels.

## Part C: interaction policy [25 pts]

Implement `reset_policy` and `choose_action`. The policy receives the cue, features, and current state. It must return an action and an updated state. Maintain at least a turn counter and last action; you may also estimate the topic/motif from dominant frequency.

Expected mapping:

```text
call      -> mirror_topic
answer    -> complement_topic
hold      -> wait
interrupt -> yield_repair
drift     -> repair_topic
end       -> close
```

The hidden grader includes multiple scripted interactions. It gives separate credit for overall action accuracy and for the drift repair rate.

## Part D: response synthesis [12 pts]

Implement `synthesize_response`. Each action should sound like its musical function, not merely be a valid waveform. The output must be a finite one-dimensional NumPy array, roughly the requested duration, and peak-normalized to [-1, 1].

| Action | Should sound like |
|--------|-------------------|
| `mirror_topic` | audibly references the topic |
| `complement_topic` | contrasts while staying related |
| `wait` | preserves space / near-silence |
| `yield_repair` | reduces density after an interruption |
| `repair_topic` | clearly returns to the topic |
| `close` | cadential / final |

The autograder checks only that each response is a valid waveform. The musical character of your six responses is assessed in the report, so aim for six distinct gestures rather than one tone reused six times.

## Part E: report and trace [20 pts]

Submit a one-page PDF report and one policy trace file. The report must include:

1. feature design;
2. classifier choice;
3. policy logic and how each action's response sound realizes its musical function;
4. one failure case or stress case;
5. a short paragraph connecting your agent to improvisation, sound poetry, or voice-agent interaction.

Include one relevant citation from the lecture readings and explain its connection. The trace can be a CSV or JSON file showing cue, predicted cue, action, and state for at least 12 turns.

## Setup

```bash
python -m venv .venv
# Windows:        .venv\Scripts\Activate.ps1
# macOS / Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

## Check your work

```bash
python check_submission.py
python check_submission.py --submission submission.py
```

This prints an 80-point breakdown using the public practice dataset in `data/`. It does not generate audio; it loads the files you were given and applies the same rubric as the real grader.

Your official grade is computed on a separate, unseen dataset of the same kind, plus 20 manual points for the written report. Treat `test/` as a held-out check, not a target.

A strong solution should reach public macro-F1 above 0.92, policy accuracy above 0.95, and drift repair rate of 1.0.

## Autograding and grade cutoffs

| Component | Points | Clear-cut criterion |
|-----------|-------:|---------------------|
| Setup / API compliance | 3 | Required file and functions exist; outputs have correct types. |
| Cue classification | 25 | Macro-F1: >= .92: 25, >= .86: 22, >= .78: 18, >= .65: 13, >= .50: 8. |
| Policy behavior | 25 | Overall policy accuracy: up to 18 points; drift repair rate: up to 7 points. |
| Response waveform | 12 | Two points per valid action waveform: finite mono array, correct duration, amplitude in range. |
| Runtime | 8 | Full hidden run: <= 20 s: 8, <= 45 s: 6, <= 90 s: 3. |
| Memory | 7 | Peak traced Python memory: <= 1 GB: 7, <= 2 GB: 5, <= 4 GB: 3. |
| Report / trace | 20 | 4 points each for feature explanation, classifier explanation, policy and response sound design, stress/failure analysis, and course/research connection with citation. |

## Submission checklist

Submit:

- `submission.py`
- one-page report PDF
- one policy trace file
- optionally one WAV example generated by `synthesize_response`

Do not submit large model weights or generated datasets. Your code should be deterministic or set random seeds.

## References

[1] UC San Diego. UCSD CSE 190 Summer 2025 Syllabus. Course website, 2025.  
[2] M. Ono. Beyond the Song Generator: How UC San Diego Students Are Rethinking AI and Music. UC San Diego Today, 2026.  
[3] X. Rojas-Rocha. New, Generative AI Transforms Poetry into Music. UC San Diego Today, 2023.  
[4] R. Rowe. *Machine Musicianship*. MIT Press, 2001.  
[5] G. E. Lewis. Too Many Notes: Computers, Complexity and Culture in Voyager. *Leonardo Music Journal*, 10:33-39, 2000.  
[6] D. Wessel and M. Wright. Problems and Prospects for Intimate Musical Control of Computers. *Computer Music Journal*, 26(3):11-22, 2002.  
[7] F. Pachet. The Continuator: Musical Interaction with Style. *Journal of New Music Research*, 32(3):333-341, 2003.  
[8] S. Dubnov. Machine Improvisation in Music: Information-Theoretical Approach. In *Handbook of Artificial Intelligence for Music*, pp. 377-408. Springer, 2021.  
[9] G. Skantze. Turn-taking in Conversational Systems and Human-Robot Interaction: A Review. *Computer Speech & Language*, 67:101178, 2021.  
[10] A. Defossez et al. Moshi: A Speech-Text Foundation Model for Real-Time Dialogue. arXiv:2410.00037, 2024.  
[11] Y. Chu et al. Qwen2-Audio Technical Report. arXiv:2407.10759, 2024.  
[12] Z. Kong et al. Audio Flamingo: A Novel Audio Language Model with Few-Shot Learning and Dialogue Abilities. ICML, 2024.  
[13] A. Goel et al. Audio Flamingo 3: Advancing Audio Intelligence with Fully Open Large Audio Language Models. arXiv:2507.08128, 2025.  
[14] A. Ivry, S. Cornell, and S. Watanabe. MAPSS: Manifold-based Assessment of Perceptual Source Separation. ICLR, 2026.  
[15] A. Ivry and S. Watanabe. LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues. ICML, 2026.  
[16] A. Ivry. Task-Aware Answer Preservation under Audio Compression for Large Audio Language Models. arXiv:2605.06631, NeurIPS, 2026 (under review).
