"""
Pre-submission crawler. Walks every internal link and audits each page against
the things an automated grader checks.

    python scripts/crawl_check.py                      # in-process, no server needed
    python scripts/crawl_check.py http://127.0.0.1:8000
    python scripts/crawl_check.py https://your.finki.ukim.mk/forge

Checks per page:
  * HTTP status is 200
  * exactly one <h1>, and heading levels never skip (h2 -> h4)
  * <title> present, non-empty, and unique across the site
  * <meta name="description"> present and non-empty
  * every <img> has an alt attribute
  * every form control has a <label for>, aria-label or aria-labelledby
  * no placeholder links (href="#", href="", javascript:void(0))
  * <html lang> is set

Site-wide:
  * every internal link resolves (no 404s)
  * both /mk/ and /en/ trees are reachable

Exit code is non-zero if anything fails, so it can gate a submission.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "#")
PLACEHOLDER_HREFS = {"#", "", "javascript:void(0)", "javascript:;"}


class Fetcher:
    """Fetches pages either over HTTP or through Django's test client."""

    def __init__(self, base_url=None):
        self.base_url = (base_url or "").rstrip("/")
        self.live = bool(base_url)

        if self.live:
            import requests

            self.session = requests.Session()
            self.session.headers["User-Agent"] = "forge-crawl-check/1.0"
        else:
            sys.path.insert(0, str(BASE_DIR))
            import os

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
            import django

            django.setup()

            import logging

            from django.conf import settings

            if "testserver" not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append("testserver")
            logging.disable(logging.CRITICAL)

            from django.test import Client

            self.client = Client(raise_request_exception=False)
            self.base_url = "http://testserver"

    def get(self, path):
        """Return (status_code, html_text)."""
        if self.live:
            resp = self.session.get(urljoin(self.base_url + "/", path.lstrip("/")),
                                    timeout=20, allow_redirects=True)
            return resp.status_code, resp.text
        resp = self.client.get(path, follow=True)
        body = resp.content.decode("utf-8", errors="replace")
        return resp.status_code, body


def is_internal(href, base_netloc):
    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return False
    if parsed.netloc and parsed.netloc != base_netloc:
        return False
    return True


def audit_page(path, html, titles):
    """Return a list of problem strings for one page."""
    problems = []
    soup = BeautifulSoup(html, "html.parser")

    # --- lang -------------------------------------------------------------
    html_tag = soup.find("html")
    if not (html_tag and html_tag.get("lang")):
        problems.append("<html> has no lang attribute")

    # --- title ------------------------------------------------------------
    title = soup.find("title")
    title_text = title.get_text(strip=True) if title else ""
    if not title_text:
        problems.append("missing or empty <title>")
    else:
        # Key on the path only. /services/ and /services/?category=x are the
        # same page filtered, so sharing a title is correct, not a duplicate.
        titles[title_text].add(urlparse(path).path)

    # --- meta description -------------------------------------------------
    desc = soup.find("meta", attrs={"name": "description"})
    if not (desc and desc.get("content", "").strip()):
        problems.append("missing or empty meta description")

    # --- headings ---------------------------------------------------------
    h1s = soup.find_all("h1")
    if len(h1s) == 0:
        problems.append("no <h1>")
    elif len(h1s) > 1:
        problems.append(f"{len(h1s)} <h1> elements (expected exactly 1)")

    levels = [int(h.name[1]) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
    for prev, curr in zip(levels, levels[1:]):
        if curr > prev + 1:
            problems.append(f"heading level skips h{prev} -> h{curr}")
            break

    # --- images -----------------------------------------------------------
    for img in soup.find_all("img"):
        if img.get("alt") is None:
            src = (img.get("src") or "?")[:60]
            problems.append(f"<img> without alt: {src}")

    # --- form controls ----------------------------------------------------
    labelled = {lbl.get("for") for lbl in soup.find_all("label") if lbl.get("for")}
    for field in soup.find_all(["input", "select", "textarea"]):
        ftype = (field.get("type") or "").lower()
        if ftype in ("hidden", "submit", "button", "image", "reset"):
            continue
        if field.get("aria-label") or field.get("aria-labelledby"):
            continue
        if field.get("id") and field["id"] in labelled:
            continue
        if field.find_parent("label"):
            continue
        name = field.get("name") or field.get("id") or field.name
        problems.append(f"form control without a label: {name}")

    # --- placeholder links ------------------------------------------------
    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        if href in PLACEHOLDER_HREFS:
            label = a.get_text(strip=True)[:40] or "(no text)"
            problems.append(f'placeholder link href="{href}" on "{label}"')

    return problems


def extract_links(html, current_path, base_netloc):
    soup = BeautifulSoup(html, "html.parser")
    out = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(SKIP_SCHEMES):
            continue
        if not is_internal(href, base_netloc):
            continue
        resolved = urljoin(current_path, href)
        out.add(urlparse(resolved)._replace(fragment="").geturl())
    return out


def check_template_comments():
    """
    Django only treats {# #} as a comment when it is on ONE line. A multi-line
    {# #} is rendered as literal text, and any tag inside it actually executes.
    That has already caused an infinite self-include and a batch of fake
    href="#" links in this project, so it is checked automatically.
    """
    bad = []
    pattern = re.compile(r"\{#(?:(?!#\}).)*$", re.M)
    for path in (BASE_DIR / "templates").rglob("*.html"):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                rel = path.relative_to(BASE_DIR).as_posix()
                bad.append(f"{rel}:{i}  multi-line {{# #}} — use {{% comment %}}")
    return bad


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else None
    fetcher = Fetcher(base_url)
    base_netloc = urlparse(fetcher.base_url).netloc

    queue = ["/mk/", "/en/"]
    seen = set()
    titles = defaultdict(set)
    failures = []
    page_problems = {}

    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        seen.add(path)

        status, html = fetcher.get(path)
        if status != 200:
            failures.append((path, status))
            print(f"FAIL {status}  {path}")
            continue

        problems = audit_page(path, html, titles)
        if problems:
            page_problems[path] = problems
            print(f"WARN 200  {path}  ({len(problems)} issue(s))")
        else:
            print(f"OK   200  {path}")

        for link in sorted(extract_links(html, path, base_netloc)):
            if link not in seen:
                queue.append(link)

    # --- report -----------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"Crawled {len(seen)} pages.")

    comment_bugs = check_template_comments()
    if comment_bugs:
        print(f"\nTemplate comment bugs ({len(comment_bugs)}):")
        for bug in comment_bugs:
            print(f"  {bug}")

    duplicate_titles = {t: p for t, p in titles.items() if len(p) > 1}

    if page_problems:
        print(f"\nPage issues ({sum(len(v) for v in page_problems.values())} total):")
        for path, problems in sorted(page_problems.items()):
            print(f"\n  {path}")
            for problem in problems:
                print(f"      - {problem}")

    if duplicate_titles:
        print(f"\nDuplicate <title> across pages ({len(duplicate_titles)}):")
        for title, paths in sorted(duplicate_titles.items()):
            print(f'  "{title[:60]}"')
            for p in paths:
                print(f"      {p}")

    if failures:
        print(f"\nBroken links ({len(failures)}):")
        for path, status in failures:
            print(f"  {status}  {path}")

    mk_pages = sum(1 for p in seen if p.startswith("/mk"))
    en_pages = sum(1 for p in seen if p.startswith("/en"))
    print(f"\nLocale coverage: {mk_pages} Macedonian, {en_pages} English")

    total_problems = (
        len(failures)
        + sum(len(v) for v in page_problems.values())
        + len(duplicate_titles)
        + len(comment_bugs)
    )
    if total_problems:
        print(f"\nFAILED — {total_problems} problem(s) to fix before submitting.")
        sys.exit(1)
    print("\nPASSED — no broken links, no accessibility or SEO issues found.")


if __name__ == "__main__":
    main()
