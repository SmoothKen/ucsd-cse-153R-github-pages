from pathlib import Path
import csv
import importlib.util
import json
import re

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
except ModuleNotFoundError as exc:
    raise SystemExit("Install the template dependency first: python -m pip install --user -r requirements.txt") from exc

root = Path(__file__).resolve().parents[1]

pages = [
    {"href": "index.html", "label": "Home", "template": "index.html", "title": "Home"},
    {"href": "syllabus.html", "label": "Syllabus", "template": "syllabus.html", "title": "Syllabus"},
    {"href": "assignments.html", "label": "Assignments", "template": "assignments.html", "title": "Assignments"},
    {"href": "resources.html", "label": "Resources", "template": "resources.html", "title": "Resources"},
]

extra_pages = [
    {"href": "404.html", "label": "", "template": "404.html", "title": "Page not found"},
]


def load_config():
    config_path = root / "course_config.py"
    spec = importlib.util.spec_from_file_location("course_config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config


def slug(text):
    text = re.sub(r"[^a-zA-Z0-9]+", "-", str(text).lower()).strip("-")
    return text or "section"


def collect_links(value, trail=()):
    if isinstance(value, dict):
        if value.get("url"):
            yield {
                "section": ".".join(trail),
                "label": value.get("label") or value.get("title") or ".".join(trail),
                "url": value["url"],
            }
        for key, child in value.items():
            yield from collect_links(child, trail + (str(key),))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from collect_links(child, trail + (str(idx),))


def write_data_files(data):
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "course.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    seen = set()
    rows = []
    for row in collect_links(data):
        key = (row["label"], row["url"])
        if key not in seen:
            rows.append(row)
            seen.add(key)

    with (data_dir / "all_links.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["section", "label", "url"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    config = load_config()
    data = config.course_data

    env = Environment(
        loader=FileSystemLoader(root / "_templates"),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["slug"] = slug

    context = {**data, "pages": pages}

    for page in pages + extra_pages:
        template = env.get_template(page["template"])
        html = template.render(
            **context,
            page_title=page["title"],
            active_page=page["label"],
        )
        (root / page["href"]).write_text(html + "\n")

    write_data_files(data)
    print("Built", ", ".join(page["href"] for page in pages + extra_pages))


if __name__ == "__main__":
    main()
