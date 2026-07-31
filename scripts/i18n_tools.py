"""
Extract translatable strings and compile .mo files WITHOUT GNU gettext.

Django's own `makemessages` / `compilemessages` shell out to xgettext and
msgfmt, which are not installed by default on Windows. This script covers the
same ground using Babel (pip-installable, lives in the venv).

    python scripts/i18n_tools.py extract   # scan sources -> locale/*/django.po
    python scripts/i18n_tools.py compile   # locale/*/django.po -> django.mo
    python scripts/i18n_tools.py stats     # how much is still untranslated

If you later install GNU gettext (winget install mlocati.GettextIconv) the
standard `manage.py makemessages -l mk -l en` and `compilemessages` will work
as normal and this script becomes optional. The .po files are compatible.
"""

import re
import sys
from pathlib import Path

from babel.messages.catalog import Catalog
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po, write_po

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / "locale"
LANGUAGES = ["mk", "en"]

SCAN_DIRS = ["templates", "core", "services", "team", "training", "blog", "contact"]
SKIP_PARTS = {"migrations", "__pycache__", "node_modules", ".git"}

# --- Patterns --------------------------------------------------------------
# Deliberately simple and explicit rather than a full template parser: this
# project only ever uses these four forms.

TRANS_RE = re.compile(r"""\{%\s*trans(?:late)?\s+(["'])(.*?)\1""", re.S)
BLOCKTRANS_RE = re.compile(
    r"""\{%\s*blocktrans(?:late)?[^%]*%\}(.*?)\{%\s*endblocktrans(?:late)?\s*%\}""", re.S
)
PY_GETTEXT_RE = re.compile(r"""\b_\(\s*(["'])(.*?)\1\s*\)""", re.S)
TEMPLATE_UNDERSCORE_RE = re.compile(r"""=_\((["'])(.*?)\1\)""", re.S)

# {{ name }} inside blocktrans becomes %(name)s in the msgid.
BLOCKTRANS_VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def normalise_blocktrans(body: str) -> str:
    """Turn a blocktrans body into the exact msgid Django will look up."""
    body = BLOCKTRANS_VAR_RE.sub(lambda m: f"%({m.group(1)})s", body)
    # `trimmed` collapses leading/trailing whitespace on every line and joins
    # them with single spaces. All our blocktrans blocks use trimmed.
    lines = [line.strip() for line in body.strip().splitlines()]
    return " ".join(line for line in lines if line)


def iter_files():
    for name in SCAN_DIRS:
        root = BASE_DIR / name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".html", ".py", ".txt"}:
                continue
            if SKIP_PARTS & set(path.parts):
                continue
            yield path


def extract():
    """Collect every msgid with the locations it appears in."""
    found = {}  # msgid -> set of "path:line"

    def add(msgid, path, offset, text):
        msgid = msgid.strip()
        if not msgid:
            return
        line = text.count("\n", 0, offset) + 1
        rel = path.relative_to(BASE_DIR).as_posix()
        found.setdefault(msgid, set()).add((rel, line))

    for path in iter_files():
        text = path.read_text(encoding="utf-8")

        if path.suffix in {".html", ".txt"}:
            for m in TRANS_RE.finditer(text):
                add(m.group(2), path, m.start(), text)
            for m in BLOCKTRANS_RE.finditer(text):
                add(normalise_blocktrans(m.group(1)), path, m.start(), text)
            for m in TEMPLATE_UNDERSCORE_RE.finditer(text):
                add(m.group(2), path, m.start(), text)
        else:
            for m in PY_GETTEXT_RE.finditer(text):
                add(m.group(2), path, m.start(), text)

    print(f"Found {len(found)} unique strings in {len(list(iter_files()))} files.")

    for lang in LANGUAGES:
        out_dir = LOCALE_DIR / lang / "LC_MESSAGES"
        out_dir.mkdir(parents=True, exist_ok=True)
        po_path = out_dir / "django.po"

        # Keep translations that already exist.
        existing = {}
        if po_path.exists():
            with po_path.open("rb") as fh:
                for msg in read_po(fh):
                    if msg.id and msg.string:
                        existing[msg.id] = msg.string

        catalog = Catalog(
            locale=lang,
            domain="django",
            project="FORGE Fitness Studio",
            charset="utf-8",
        )
        for msgid in sorted(found):
            # English is the source language, so every English msgstr is the
            # msgid itself — that keeps the catalog complete and lets Django
            # fall through cleanly.
            default = msgid if lang == "en" else ""
            catalog.add(
                msgid,
                string=existing.get(msgid, default),
                locations=sorted(found[msgid]),
            )

        with po_path.open("wb") as fh:
            write_po(fh, catalog, width=88, sort_output=True)

        translated = sum(1 for m in catalog if m.id and m.string)
        print(f"  {lang}: wrote {po_path.relative_to(BASE_DIR)} "
              f"({translated}/{len(found)} translated)")


def apply_translations():
    """Merge scripts/mk_translations.py into locale/mk/LC_MESSAGES/django.po."""
    sys.path.insert(0, str(BASE_DIR / "scripts"))
    from mk_translations import MK

    po_path = LOCALE_DIR / "mk" / "LC_MESSAGES" / "django.po"
    with po_path.open("rb") as fh:
        catalog = read_po(fh, locale="mk", domain="django")

    applied = unknown = 0
    for msg in catalog:
        if not msg.id:
            continue
        if msg.id in MK:
            msg.string = MK[msg.id]
            applied += 1

    catalog_ids = {m.id for m in catalog if m.id}
    stale = sorted(set(MK) - catalog_ids)
    unknown = len(stale)

    with po_path.open("wb") as fh:
        write_po(fh, catalog, width=88, sort_output=True)

    total = len(catalog_ids)
    print(f"Applied {applied}/{total} Macedonian translations.")
    if stale:
        print(f"\n{unknown} entries in mk_translations.py match no msgid "
              f"(source string changed?):")
        for msgid in stale[:15]:
            print(f"   STALE  {msgid[:80]}")

    missing = sorted(m.id for m in catalog if m.id and not m.string)
    if missing:
        print(f"\n{len(missing)} strings still untranslated:")
        for msgid in missing[:25]:
            print(f"   TODO  {msgid[:80]}")
        if len(missing) > 25:
            print(f"   … and {len(missing) - 25} more")


def compile_catalogs():
    for lang in LANGUAGES:
        po_path = LOCALE_DIR / lang / "LC_MESSAGES" / "django.po"
        if not po_path.exists():
            print(f"  {lang}: no django.po — run 'extract' first")
            continue

        with po_path.open("rb") as fh:
            catalog = read_po(fh, locale=lang, domain="django")

        mo_path = po_path.with_suffix(".mo")
        with mo_path.open("wb") as fh:
            write_mo(fh, catalog)

        total = sum(1 for m in catalog if m.id)
        done = sum(1 for m in catalog if m.id and m.string)
        print(f"  {lang}: compiled {mo_path.relative_to(BASE_DIR)} ({done}/{total})")


def stats():
    for lang in LANGUAGES:
        po_path = LOCALE_DIR / lang / "LC_MESSAGES" / "django.po"
        if not po_path.exists():
            print(f"{lang}: missing")
            continue
        with po_path.open("rb") as fh:
            catalog = read_po(fh)
        missing = [m.id for m in catalog if m.id and not m.string]
        total = sum(1 for m in catalog if m.id)
        print(f"\n{lang}: {total - len(missing)}/{total} translated")
        for msgid in missing[:40]:
            print(f"   MISSING  {msgid[:88]}")
        if len(missing) > 40:
            print(f"   … and {len(missing) - 40} more")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "extract"
    if command == "extract":
        extract()
    elif command == "apply":
        apply_translations()
    elif command == "compile":
        compile_catalogs()
    elif command == "stats":
        stats()
    else:
        print(__doc__)
        sys.exit(1)
