# FORGE Fitness Studio

Bilingual presentation website for a fictional gym in Skopje, built for the
**Business Practice 2025/2026** course at FCSE.

Django 5.2 · Bootstrap 5.3 · HTMX · SQLite · WhiteNoise — no Node build step.

---

## Quick start

```bash
py -3.13 -m venv venv
```

```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

```bash
copy .env.example .env
```

Generate a key and paste it into `.env` as `SECRET_KEY`:

```bash
venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

```bash
venv\Scripts\python.exe manage.py migrate
```

```bash
venv\Scripts\python.exe manage.py seed_demo
```

```bash
venv\Scripts\python.exe manage.py createsuperuser
```

```bash
venv\Scripts\python.exe manage.py runserver
```

Then open http://127.0.0.1:8000/ — admin is at `/admin/`.

> **`.env` must be saved without a UTF-8 BOM.** PowerShell's `-Encoding utf8` adds one,
> and `django-environ` then silently fails to read the first line, so `DEBUG` falls
> back to `False`. Use an editor set to "UTF-8 without BOM".

---

## Assignment requirements → where they live

| Requirement | Where |
|---|---|
| Basic information | `/` and `/about/` — `core` app |
| Team / employees | `/team/` + a detail page per trainer — `team` app |
| Services | `/services/` + a detail page per service — `services` app |
| Contact form | `/contact/` — `contact` app, saves to DB, HTMX submit |
| Contact information | Footer, `/contact/`, OpenStreetMap embed |
| News / blog | `/blog/` — pagination, category filter, live search |
| Multilingual | `/mk/` and `/en/` — gettext **and** django-modeltranslation |
| Cookies | Consent banner + `/privacy/` listing every cookie set |
| Detailed information | Detail pages for services, trainers, classes and posts |
| Entity-specific | Weekly class schedule, membership plans, class booking |

---

## Project layout

```
config/          settings split into base / dev / prod, URLs, WSGI
core/            SiteSettings singleton, opening hours, testimonials, FAQ, sitemaps
services/        service catalogue with categories and galleries
team/            trainers and their specialties
training/        classes, weekly schedule sessions, membership plans   <- gym-specific
blog/            posts, categories, search
contact/         contact form + booking form, honeypot spam protection
templates/       base.html + one folder per app + shared partials/
static/css/      theme.css — the brand layer over Bootstrap
static/js/       main.js — cookie consent, scroll reveal
locale/          mk/ and en/ translation catalogues
seed_assets/     photos seed_demo attaches; committed because media/ is gitignored
scripts/         smoke_check, crawl_check, i18n_tools, mk_translations
```

---

## Commands

Seed realistic bilingual content (idempotent; `--flush` wipes first):

```bash
venv\Scripts\python.exe manage.py seed_demo
```

Run the test suite:

```bash
venv\Scripts\python.exe manage.py test
```

Check every URL returns 200, in both languages:

```bash
venv\Scripts\python.exe scripts\smoke_check.py
```

Full crawl + accessibility/SEO audit — **run this before submitting**:

```bash
venv\Scripts\python.exe scripts\crawl_check.py
```

---

## Translations

Two mechanisms, both required:

- **UI strings** — `{% trans %}` / `gettext`, compiled into `locale/*/LC_MESSAGES/django.mo`
- **Database content** — `django-modeltranslation` adds `_mk` / `_en` columns, edited
  as tabs in the admin

Without the second one, switching to English would still show Macedonian services and
blog posts. This is the most common way the multilingual requirement half-fails.

GNU gettext is not installed on most Windows machines, so `scripts/i18n_tools.py`
does the same job using Babel (already in the venv):

```bash
venv\Scripts\python.exe scripts\i18n_tools.py extract
```

```bash
venv\Scripts\python.exe scripts\i18n_tools.py apply
```

```bash
venv\Scripts\python.exe scripts\i18n_tools.py compile
```

Macedonian translations live in `scripts/mk_translations.py`. Add a new UI string by
wrapping it in `{% trans %}`, then running `extract` → adding it to that file →
`apply` → `compile`.

`.po` files are committed; `.mo` files are build artefacts and are gitignored, so
**compile on the server after every deploy** or the site renders in English.

---

## Deployment

See **[DEPLOY.md](DEPLOY.md)**.

---

