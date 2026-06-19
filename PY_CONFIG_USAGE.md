# Python-config course site workflow

The source of truth is now:

```text
course_config.py
```

Edit normal Python variables there, for example:

```python
course = "190"
professor = "Shlomo Dubnov"
ta = "Girish Krishnan"
required_assignments[0]["due"] = "7/5"
```

Then regenerate the static HTML:

```bash
python3 scripts/build_site.py
```

or:

```bash
scripts/rebuild_site.sh
```

Then push using the existing shell function from `audio_snippets.sh`:

```bash
update_github_repo
```

One-line update flow:

```bash
scripts/rebuild_site.sh && update_github_repo
```

GitHub Pages serves static files and does not execute Python server-side. The Python config is therefore a build-time source, and `build_site.py` writes `index.html`, `syllabus.html`, `assignments.html`, `resources.html`, `404.html`, and `data/all_links.csv`.

The previous `data/course.json` can be kept for archive/history, but it is no longer used by `scripts/build_site.py`.
