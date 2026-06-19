# UCSD CSE 190 GitHub Pages site

Static GitHub Pages version of **UCSD CSE 190: Machine Learning for Music & Audio**.

The source of truth for course content is now `course_config.py`. Edit variables there, rebuild the static HTML, then push.

## Fast update flow

```bash
scripts/rebuild_site.sh && update_github_repo
```

This matches the existing `update_github_repo` helper style: it adds all files, commits with a timestamp, and force-pushes to `origin master`.

## First push

```bash
git init
git remote add origin git@github.com:SmoothKen/ucsd-cse-190-github-pages.git
scripts/rebuild_site.sh
git add .
git commit -m "Initial course site"
git push -f origin master
scripts/enable_github_pages.sh
```

## Editing

Most edits should happen in:

```text
course_config.py
```

Examples:

```python
course = "190"
term = "Summer 2025"
professor = "Shlomo Dubnov"
ta = "Girish Krishnan"
required_assignments[0]["due"] = "7/5"
optional_due = "8/1"
```

Then rebuild:

```bash
python3 scripts/build_site.py
```

The generated public files are:

- `index.html`
- `syllabus.html`
- `assignments.html`
- `resources.html`
- `404.html`
- `data/all_links.csv`

`data/course.json` can remain as an old archive file, but it is no longer used.

## Preview locally

```bash
scripts/preview.sh
```

Open <http://localhost:8000>.

## Link checks

```bash
python3 scripts/check_links.py
```

Some Google Drive, Canvas, Zoom, and course-private links may require UCSD login or course access. Treat those as permission checks rather than necessarily broken public links.

## Files and images

Place any professor-provided PDFs, images, notebooks, or handouts under `assets/files/` if you want them served directly by GitHub Pages. Restricted Google Drive resources are intentionally preserved as external links.
