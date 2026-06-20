test -f README.md
test -d autograder
test -d solution
test -d student_release
test -d scripts
test -d docs
test -d tests

find . -maxdepth 2 \( -name pyproject.toml -o -name poetry.lock \) -print

poetry run python - <<'PY'
from pathlib import Path

print("python files:", len(list(Path(".").rglob("*.py"))))
print("wav files:", len(list(Path(".").rglob("*.wav"))))
print("student train wavs:", len(list(Path("student_release/data/train").glob("*.wav"))))
print("student test wavs:", len(list(Path("student_release/data/test").glob("*.wav"))))

expected = [
    "README.md",
    "requirements.txt",
    "MANIFEST.md",
    "autograder/sonic_dataset.py",
    "autograder/autograde.py",
    "autograder/batch_grade.py",
    "solution/submission.py",
    "scripts/create_dataset.py",
    "scripts/run_reference_solution.py",
    "scripts/validate_package.py",
    "scripts/make_student_release_zip.py",
    "scripts/export_student_data.py",
    "student_release/submission.py",
    "student_release/check_submission.py",
    "student_release/sonic_data.py",
    "student_release/README.md",
    "student_release/requirements.txt",
    "student_release/data/labels.csv",
    "student_release/data/sequences.json",
    "tests/test_api_smoke.py",
    "docs/TA_RUNBOOK.md",
    "docs/OFFICIAL_SOLUTION.md",
    "docs/GRADING_CONTRACT.md",
    "docs/REPORT_RUBRIC.md",
    "docs/HARDWARE_VALIDATION.md",
    "docs/RELEASE_CHECKLIST.md",
]

missing = [p for p in expected if not Path(p).exists()]
print("missing:", missing)
PY

rg -n "^(def|class) |if __name__|argparse|TODO|FIXME|NotImplemented|pass$" -S . -g '!student_release/data/**'