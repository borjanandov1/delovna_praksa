import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

import logging  # noqa: E402

from django.conf import settings  # noqa: E402

if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append("testserver")

logging.disable(logging.CRITICAL)

from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from blog.models import Post  # noqa: E402
from services.models import Service  # noqa: E402
from team.models import TeamMember  # noqa: E402
from training.models import GymClass  # noqa: E402

STATIC_ROUTES = [
    "core:home",
    "core:about",
    "core:faq",
    "core:privacy",
    "core:terms",
    "services:list",
    "team:list",
    "training:class_list",
    "training:schedule",
    "training:pricing",
    "blog:list",
    "contact:contact",
    "contact:booking",
]


def collect_urls():
    urls = [reverse(name) for name in STATIC_ROUTES]
    for model in (Service, TeamMember, GymClass, Post):
        for obj in model.objects.all()[:3]:
            urls.append(obj.get_absolute_url())
    return urls


def fetch(client, path):
    try:
        resp = client.get(path)
        return resp.status_code, ""
    except Exception as exc:
        return 500, f"{type(exc).__name__}: {exc}"


def main():
    client = Client(raise_request_exception=True)
    failures = []
    checked = 0

    for path in ["/sitemap.xml", "/robots.txt"]:
        status, err = fetch(client, path)
        checked += 1
        print(f"{'OK ' if status == 200 else 'FAIL'} {status}  {path}  {err}")
        if status != 200:
            failures.append((path, status, err))

    for lang in ("mk", "en"):
        print(f"\n--- /{lang}/ " + "-" * 50)
        for url in collect_urls():
            path = "/" + lang + url[3:] if url.startswith(("/mk", "/en")) else url
            status, err = fetch(client, path)
            checked += 1
            print(f"{'OK ' if status == 200 else 'FAIL'} {status}  {path}  {err}")
            if status != 200:
                failures.append((path, status, err))

    print("\n" + "=" * 60)
    if failures:
        print(f"{len(failures)} of {checked} URLs failed:")
        for path, status, err in failures:
            print(f"  {status}  {path}\n        {err}")
        sys.exit(1)
    print(f"All {checked} URLs returned 200.")


if __name__ == "__main__":
    main()
