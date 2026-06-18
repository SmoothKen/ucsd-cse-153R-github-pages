# UCSD CSE 190 GitHub Pages site

Static GitHub Pages version of **UCSD CSE 190: Machine Learning for Music & Audio**.

This package is designed to be unzipped into an empty GitHub repository and pushed as-is. It uses plain HTML/CSS/JS and includes `.nojekyll`, so there is no Ruby, Node, Jekyll, npm, or build dependency for serving the current site.

## Fast path

```bash
unzip ucsd-cse-190-github-pages.zip
cd ucsd-cse-190-github-pages

git init
git add .
git commit -m "Initial course site"
git branch -M main
git remote add origin git@github.com:OWNER/REPO.git
git push -u origin main
```

Then enable GitHub Pages from the repository root:

```bash
scripts/enable_github_pages.sh OWNER REPO main
```

The script uses the GitHub CLI (`gh`) and configures Pages to serve from the `main` branch root (`/`). You can also do the same manually in GitHub: Settings → Pages → Deploy from a branch → `main` → `/`.

## Editing

For simple updates, edit the visible HTML files directly and push.

For structured updates, edit `data/course.json`, then rebuild:

```bash
python3 scripts/build_site.py
```

The generated public pages are:

- `index.html`
- `syllabus.html`
- `assignments.html`
- `resources.html`
- `404.html`

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

No first-party JPG/PDF/course-asset files were exposed as downloadable public files during extraction. Restricted Google Drive files remain as links. If you receive local PDFs/JPGs from the professor or TA, place them under `assets/files/` and update the relevant URLs in `data/course.json` or the generated HTML.

## Recommended ownership model

Use a professor-, lab-, or department-owned GitHub organization/repository. Add TAs with write access, require pull requests if desired, and keep sensitive materials such as solutions, grades, submissions, and restricted recordings in Canvas/Gradescope/Drive rather than this public site.
