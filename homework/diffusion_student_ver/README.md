# Diffusion HW4 Student Handout

Run all commands from this folder:

```bash
cd homework/diffusion_student_ver
python -m pip install -r requirements.txt
```

This handout includes a local bundled `stable_audio_tools/` package. The notebook
uses helper functions from that bundled package that are not available in the
public `stable-audio-tools==0.0.19` PyPI release.

If the setup cell cannot import:

```python
generate_diffusion_cond_and_sampler_setup
generate_diffusion_cond_decode
```

then the notebook kernel is importing the PyPI package instead of this local
assignment package. Re-run:

```bash
python -m pip install -r requirements.txt
```

then restart the notebook kernel.

You can verify the import path with:

```bash
python - <<'PY'
import stable_audio_tools.inference.generation as g
print(g.__file__)
print(hasattr(g, "generate_diffusion_cond_and_sampler_setup"))
print(hasattr(g, "generate_diffusion_cond_decode"))
PY
```

The printed path should point inside this `diffusion_student_ver` folder.
