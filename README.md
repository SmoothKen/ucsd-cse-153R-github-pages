# UCSD CSE 153R GitHub Pages site

Static GitHub Pages version of **UCSD CSE 153R: Machine Learning for Music & Audio**.


## First push (one time)

```bash
git init
git remote add origin git@github.com:SmoothKen/ucsd-cse-153R-github-pages.git
python3 scripts/build_site.py
git add .
git commit -m "Initial course site"
git push -f origin master
scripts/enable_github_pages.sh
```

## Editing/Maintenance

Most edits should happen in `course_config.py`:

Examples:

```python
course = "190"
term = "Summer 2025"
professor = "Shlomo Dubnov"
ta = "Keren Shao"
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

Then add/commit/push to update the repo.

## Link checks

```bash
python3 scripts/check_links.py
```

Some Google Drive, Canvas, Zoom, and course-private links may require UCSD login or course access. Treat those as permission checks rather than necessarily broken public links.

## Files and images

Place any professor-provided PDFs, images, notebooks, or handouts under `assets/files/` if you want them served directly by GitHub Pages. Restricted Google Drive resources are intentionally preserved as external links.
