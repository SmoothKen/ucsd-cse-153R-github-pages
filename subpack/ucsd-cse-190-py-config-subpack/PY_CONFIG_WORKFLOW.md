# Python-config course site workflow

Edit `course_config.py`, then rebuild the static HTML files:

```bash
scripts/rebuild_site.sh
```

With your existing shell helper loaded, this can be the whole update flow:

```bash
scripts/update_site.sh
```

If `update_github_repo` is a shell function that is only available in your interactive shell, this also works:

```bash
scripts/rebuild_site.sh
update_github_repo
```

The build rewrites:

- `index.html`
- `syllabus.html`
- `assignments.html`
- `resources.html`
- `404.html`
- `data/course.json`
- `data/all_links.csv`

The editable source of truth is `course_config.py`. The HTML layout is in `_templates/`.
