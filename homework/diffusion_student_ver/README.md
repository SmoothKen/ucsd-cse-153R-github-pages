# HW4 Diffusion Assignment

## What This Is

This is the student-facing HW4 package for audio diffusion. It uses Stable Audio to test latent-space diffusion operations without requiring students to submit generated audio.

The required notebook is:

```text
homework4_diffusion_assignment.ipynb
```

Run the notebook from this folder. The folder must contain:

- `homework4_diffusion_assignment.ipynb`
- `stable_audio_tools/`
- `testing_files/`
- `x_T.pt`
- `references/`

## Learning Goals

- Implement a simple Euler sampler for reverse diffusion.
- Create an inpainting mask in latent time.
- Use a reference latent and mask for audio inpainting.
- Control when inpainting is applied during the diffusion process.
- Implement style transfer by starting from a partially noised reference latent.

## Hugging Face Setup

This assignment uses the gated model:

```text
stabilityai/stable-audio-open-1.0
```

Before running the notebook:

1. Create or use a Hugging Face account.
2. Open `https://huggingface.co/stabilityai/stable-audio-open-1.0`.
3. Accept/request access to the model.
4. Create a read token at `https://huggingface.co/settings/tokens`.
5. Set the token in your terminal or DataHub session:

```bash
export HF_TOKEN='paste-your-token-here'
```

Do not paste your token into a notebook cell and do not submit it.

## Environment Check

From this folder, run:

```bash
python hw4_preflight.py
python hw4_model_smoke.py
```

`hw4_preflight.py` checks package imports, Hugging Face model access, and local test files.

`hw4_model_smoke.py` downloads/loads the Stable Audio model. The first run can take several minutes.

## Running The Assignment

Open and run:

```text
homework4_diffusion_assignment.ipynb
```

Complete Q1-Q5. Each question has a latent MSE check against the reference tensors in `testing_files/`.

Low MSE means your implementation matches the expected latent behavior. Audio playback cells are optional and GPU-recommended.

## GPU / CPU Notes

A GPU is strongly recommended. CPU can run the latent tests but is slow. Full audio generation is optional and should not be required on CPU.

The Stable Audio model cache is about 4.5 GB. A practical working budget is at least 8-10 GB of available disk/cache space.
