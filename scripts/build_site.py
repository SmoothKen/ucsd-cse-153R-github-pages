from pathlib import Path
import csv
import html
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

import course_config as cfg

data = cfg.course_data
site = data["site"]

pages = [
    ("index.html", "Home"),
    ("syllabus.html", "Syllabus"),
    ("assignments.html", "Assignments"),
    ("resources.html", "Resources"),
]

def esc(x):
    return html.escape(str(x), quote=True)

def link(label, url, cls=""):
    c = f' class="{esc(cls)}"' if cls else ""
    return f'<a{c} href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'

def nav(active):
    items = []
    for href, label in pages:
        cls = ' class="active" aria-current="page"' if label == active else ""
        items.append(f'<a{cls} href="{href}">{label}</a>')
    return "\n".join(items)

def shell(title, active, body):
    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(title)} | {esc(site["short_title"])}</title>
    <meta name="description" content="{esc(site["description"])}">
    <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
    <a class="skip" href="#main">Skip to main content</a>
    <header class="site-header">
        <div class="container header-grid">
            <a class="brand" href="index.html">
                <span class="brand-mark">{esc(cfg.course)}</span>
                <span>
                    <strong>{esc(site["short_title"])}</strong>
                    <small>{esc(site["term"])}</small>
                </span>
            </a>
            <nav class="nav" aria-label="Primary navigation">
                {nav(active)}
            </nav>
        </div>
    </header>
    <main id="main" class="container page">
        {body}
    </main>
    <script src="assets/js/site.js"></script>
</body>
</html>
'''

def home_page():
    people = "\n".join(
        f'''<article class="card">
            <p class="eyebrow">{esc(p["role"])}</p>
            <h3>{esc(p["name"])}</h3>
            <p><a href="mailto:{esc(p["email"])}">{esc(p["email"])}</a></p>
            <p>{esc(p["office_hours"])}</p>
            <p>{link("Zoom link", p["office_hours_url"], "button")}</p>
        </article>'''
        for p in data["people"]
    )
    course_links = "\n".join(
        f'<li><strong>{link(x["label"], x["url"])}</strong><span>{esc(x.get("note", ""))}</span></li>'
        for x in data["course_links"]
    )
    notes = "\n".join(f'<li>{esc(x)}</li>' for x in data["home_notes"])
    body = f'''
        <section class="hero">
            <p class="eyebrow">{esc(site["term"])}</p>
            <h1>{esc(site["title"])}</h1>
            <p class="lede">A static, version-controlled course site for public course information, assignments, resources, and lecture links.</p>
            <div class="hero-actions">
                <a class="button" href="assignments.html">View assignments</a>
                <a class="button secondary" href="syllabus.html">View syllabus</a>
            </div>
        </section>

        <section aria-labelledby="people">
            <div class="section-heading">
                <p class="eyebrow">Contacts</p>
                <h2 id="people">Course staff</h2>
            </div>
            <div class="card-grid two">{people}</div>
        </section>

        <section aria-labelledby="course-links">
            <div class="section-heading">
                <p class="eyebrow">Course systems</p>
                <h2 id="course-links">Useful links</h2>
            </div>
            <ul class="link-list">{course_links}</ul>
        </section>

        <section class="callout" aria-labelledby="course-notes">
            <h2 id="course-notes">Course notes</h2>
            <ul>{notes}</ul>
        </section>
    '''
    return shell("Home", "Home", body)

def syllabus_page():
    notes = "\n".join(f'<li>{esc(x)}</li>' for x in data["syllabus"]["recording_notes"])
    week_html = []
    for week in data["weeks"]:
        classes = []
        for c in week["classes"]:
            slide_html = ""
            if c.get("slides"):
                slide_html = '<p class="resource-line">' + " · ".join(link(s["label"], s["url"], "pill") for s in c["slides"]) + '</p>'
            items = []
            for item in c.get("items", []):
                label = link(item["label"], item["url"]) if item.get("url") else esc(item["label"])
                note = f' <span class="muted">({esc(item["note"])})</span>' if item.get("note") else ""
                items.append(f'<li>{label}{note}</li>')
            classes.append(f'''<article class="class-card searchable">
                <h3>{esc(c["title"])}</h3>
                {slide_html}
                <ul>{"".join(items)}</ul>
            </article>''')
        week_id = esc(week["week"].lower().replace(" ", "-"))
        week_html.append(f'''<section class="week" aria-labelledby="{week_id}">
            <h2 id="{week_id}">{esc(week["week"])}</h2>
            <div class="class-grid">{"".join(classes)}</div>
        </section>''')
    body = f'''
        <section class="page-title">
            <p class="eyebrow">Syllabus</p>
            <h1>Schedule and lecture materials</h1>
            <p class="lede">Lecture recordings, slide links, prerequisites, and course description.</p>
        </section>

        <section class="card-grid two">
            <article class="card">
                <p class="eyebrow">Prerequisite</p>
                <p>{esc(data["syllabus"]["prerequisite"])}</p>
            </article>
            <article class="card">
                <p class="eyebrow">Enrollment</p>
                <p>{esc(data["syllabus"]["enrollment"])}</p>
            </article>
        </section>

        <section>
            <h2>Description</h2>
            <p>{esc(data["syllabus"]["description"])}</p>
        </section>

        <section class="callout">
            <h2>Recording notes</h2>
            <ul>{notes}</ul>
        </section>


        <section class="toolbar" aria-label="Schedule search">
            <label for="schedule-search">Filter schedule</label>
            <input id="schedule-search" type="search" placeholder="Search videos, topics, weeks, or classes">
        </section>

        {"".join(week_html)}
    '''
    return shell("Syllabus", "Syllabus", body)

def assignment_rows(items, include_dates=True):
    rows = []
    for a in items:
        title = link(a["title"], a["url"]) if a.get("url") else esc(a["title"])
        topic = f'<span class="muted">{esc(a["topic"])}</span><br>' if a.get("topic") else ""
        if a.get("options"):
            opts = " · ".join(link(o["label"], o["url"]) for o in a["options"])
            title = f'{esc(a["title"])}<br><span class="subtle">{opts}</span>'
        date_cols = f'<td>{esc(a.get("due", "8/1"))}</td><td>{esc(a.get("self_grade_due", "8/4"))}</td>' if include_dates else ""
        rows.append(f'<tr><td>{esc(a["number"])}</td><td>{topic}{title}</td>{date_cols}</tr>')
    return "\n".join(rows)

def assignments_page():
    assn = data["assignments"]
    required = assignment_rows(assn["required"])
    optional = assignment_rows([{**a, "due": assn["optional_due"], "self_grade_due": assn["optional_self_grade_due"]} for a in assn["optional"]])
    milestones = "\n".join(f'<li><strong>{esc(m["label"])}</strong> ({esc(m["weight"])}) due {esc(m["due"])}</li>' for m in assn["project"]["milestones"])
    self_grading = "\n".join(f'<li>{esc(x)}</li>' for x in assn["self_grading"]["instructions"])
    body = f'''
        <section class="page-title">
            <p class="eyebrow">Assignments</p>
            <h1>Homework and final project</h1>
            <p class="lede">Programming assignments, optional assignment track, final project track, and self-grading instructions.</p>
        </section>

        <section>
            <h2>Required assignments</h2>
            <p>{esc(assn["required_intro"])}</p>

            <div class="table-wrap">
                <table>
                    <thead><tr><th>#</th><th>Assignment</th><th>Due</th><th>Self-grades due</th></tr></thead>
                    <tbody>{required}</tbody>
                </table>
            </div>
        </section>

        <section>
            <h2>Remaining 40%: choose assignments or project</h2>
            <p>{esc(assn["choice_intro"])}</p>
            <article class="card">
                <h3>Option 1: Assignments</h3>
                <p>Choose 4 of these 5 assignments. Each assignment is worth 10% of the grade. Due {esc(assn["optional_due"])}, with self-grading due {esc(assn["optional_self_grade_due"])}.</p>
                <div class="table-wrap">
                    <table>
                        <thead><tr><th>#</th><th>Assignment</th><th>Due</th><th>Self-grades due</th></tr></thead>
                        <tbody>{optional}</tbody>
                    </table>
                </div>
            </article>
            <article class="card">
                <h3>Option 2: {link(assn["project"]["title"], assn["project"]["url"])}</h3>
                <ul>{milestones}</ul>
                <p>To get an idea of projects done in previous quarters, see {link("this folder", assn["project"]["previous_projects_url"])}.</p>
            </article>
        </section>

        <section class="callout">
            <h2>Self-grading instructions</h2>
            <p>The point of homework in this class is to learn the material. Students must evaluate their own homework in addition to TA grading. Self-grading is mandatory to receive credit for an assignment.</p>
            <p>{link("Self-Grading Form", assn["self_grading"]["form_url"], "button")}</p>
            <ol>{self_grading}</ol>
            <p>If you have any questions, please ask on Piazza.</p>
        </section>
    '''
    return shell("Assignments", "Assignments", body)

def resources_page():
    resources = "\n".join(
        f'<li><strong>{link(x["label"], x["url"])}</strong><span>{esc(x.get("note", ""))}</span></li>'
        for x in data["resources"]
    )
    fun = "\n".join(f'<li>{link(x["label"], x["url"])}</li>' for x in data["fun_resources"])
    body = f'''
        <section class="page-title">
            <p class="eyebrow">Resources</p>
            <h1>Readings, videos, and external references</h1>
        </section>
        <section>
            <h2>Course resources</h2>
            <ul class="link-list">{resources}</ul>
        </section>
        <section>
            <h2>Other fun stuff</h2>
            <ul class="link-list compact">{fun}</ul>
        </section>
    '''
    return shell("Resources", "Resources", body)

def not_found_page():
    body = '''
        <section class="page-title">
            <p class="eyebrow">404</p>
            <h1>Page not found</h1>
            <p class="lede">The page may have moved. Use the navigation above or return to the home page.</p>
            <p><a class="button" href="index.html">Go home</a></p>
        </section>
    '''
    return shell("Page not found", "", body)

def write_link_csv():
    rows = []

    def walk(obj, path=""):
        if isinstance(obj, dict):
            if "url" in obj:
                rows.append([path.strip("/"), obj.get("label") or obj.get("title") or obj.get("name") or "", obj["url"], obj.get("note", "")])
            for k, v in obj.items():
                walk(v, f"{path}/{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}/{i}")

    walk(data)
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    with (data_dir / "all_links.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_path", "label", "url", "note"])
        w.writerows(rows)

def repo_name():
    return f"{cfg.institution.lower()}-{cfg.department.lower()}-{cfg.course}-github-pages"

def readme_page():
    return f"""# {site["short_title"]} GitHub Pages site

Static GitHub Pages version of **{site["title"]}**.

> Generated by `python3 scripts/build_site.py` from `scripts/course_config.py`; edit the config, not this file.

## First push (one time)

```bash
git init
git remote add origin git@github.com:SmoothKen/{repo_name()}.git
python3 scripts/build_site.py
git add .
git commit -m "Initial course site"
git push -f origin master
scripts/enable_github_pages.sh
```

## Editing/Maintenance

Most edits should happen in `scripts/course_config.py`.

Current course identity is assembled from:

```python
institution = {cfg.institution!r}
department = {cfg.department!r}
course = {cfg.course!r}
term = {site["term"]!r}
topic = {cfg.topic!r}
```

Then rebuild:

```bash
python3 scripts/build_site.py
```

The generated/rebuilt files are:

- `index.html`
- `syllabus.html`
- `assignments.html`
- `resources.html`
- `404.html`
- `data/all_links.csv`
- `README.md`
- `LICENSE_NOTICE.md`

Then add/commit/push to update the repo.

## Link checks

```bash
python3 scripts/check_links.py
```

Some Google Drive, Canvas, Zoom, and course-private links may require UCSD login or course access. Treat those as permission checks rather than necessarily broken public links.

## Files and images

Place any professor-provided PDFs, images, notebooks, or handouts under `assets/files/` if you want them served directly by GitHub Pages. Restricted Google Drive resources are intentionally preserved as external links.

"""

def license_notice_page():
    return f"""# License notice

This repository is a migration scaffold for **{site["title"]}**.

This notice does not assert ownership over UCSD, instructor, TA, textbook, Google Drive, YouTube, GitHub, Zoom, Canvas, Gradescope, Piazza, or third-party materials linked from the site.

Before publishing under a long-term repository, have the professor or department confirm that public course text and links are intended to remain public.

The small static-site scaffolding files in this package (`assets/css/site.css`, `assets/js/site.js`, and scripts under `scripts/`) may be reused and modified for the course migration.
"""

def write_markdown_docs():
    docs = {
        "README.md": readme_page(),
        "LICENSE_NOTICE.md": license_notice_page(),
    }
    for name, text in docs.items():
        (root / name).write_text(text, encoding="utf-8")

outputs = {
    "index.html": home_page(),
    "syllabus.html": syllabus_page(),
    "assignments.html": assignments_page(),
    "resources.html": resources_page(),
    "404.html": not_found_page(),
}

for name, text in outputs.items():
    (root / name).write_text(text, encoding="utf-8")

write_link_csv()
write_markdown_docs()
print("Built", ", ".join([*outputs, "README.md", "LICENSE_NOTICE.md"]))
