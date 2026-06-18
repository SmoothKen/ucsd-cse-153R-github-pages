# Setup checklist

## One-time repository setup

1. Create an empty GitHub repository under the long-term owner: professor, lab, course, or department organization.
2. Unzip this package into the repository.
3. Commit and push the files.
4. Enable GitHub Pages from the branch root.

```bash
git init
git add .
git commit -m "Initial course site"
git branch -M main
git remote add origin git@github.com:OWNER/REPO.git
git push -u origin main
scripts/enable_github_pages.sh OWNER REPO main
```

## Suggested permissions

- Professor: repository admin or organization owner
- Lead TA: maintain
- Other TAs: write
- Students: public read access only

## Safe update flow

1. TA edits `data/course.json` or a page.
2. TA rebuilds if data changed: `python3 scripts/build_site.py`.
3. TA opens a pull request.
4. Professor reviews or edits directly.
5. Merge to `main`; GitHub Pages updates from the branch root.

## What should stay out of this repo

- Student data
- Grades
- Assignment submissions
- Private Zoom recordings
- Solutions or hidden rubrics unless the repository is private and Pages visibility is appropriate
- Drive files whose sharing permissions should remain course-restricted
