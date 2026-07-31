# Business Practice 2025/2026 — Project Plan

Presentation website for a small business, built with **Django + Bootstrap 5**, deployed on the FCSE system.

---

## 0. Read this first: what actually earns the points

The grading is 100 points across four sources. Design your work around the *scoring*, not around "make a nice website".

| Points | Source | What actually moves the needle |
|---|---|---|
| **50** | Teacher, at a live presentation | Completeness of required elements, working forms, working multilingual, working admin, a confident 10-min demo |
| **30** | 3+ classmates rate you 0–5 | **Visual polish and first impression.** Classmates spend ~3 minutes and judge on looks, speed, mobile, and whether anything is obviously broken |
| **10** | You review 3 other projects | Free points. Just do it, with real written justification. Do not forget this — it's the easiest 10 points on the course |
| **10** | An automated agent crawls all pages and elements | **Zero 404s, zero broken links, every nav item resolves, valid semantic HTML, alt text on every image, forms with proper labels/names, both languages reachable** |

**Two consequences that shape every decision below:**

1. The agent check means *technical correctness of every link and element* is worth as much as a whole feature. Build a link-crawler self-test (§10) and run it before submission.
2. The 30 peer points are decided in ~3 minutes of skimming. So: fast load, real photos, a custom color theme that does **not** look like stock Bootstrap, and perfect mobile layout. A technically deep site that looks like a default Bootstrap template will lose these points to a shallower site that looks designed.

**Requirement checklist straight from the assignment** (every one of these must exist, and must be reachable from the nav):

- [ ] Basic information about the entity
- [ ] Team / employees
- [ ] Services
- [ ] Contact form (must actually submit and persist)
- [ ] Contact information
- [ ] News / blog
- [ ] Multilingual support
- [ ] Cookie consent
- [ ] "Detailed information" — deeper detail pages, not just landing sections
- [ ] Entity-specific elements (the differentiator — see §2)

---

## 1. Tech stack

### Recommended (what I'd build)

| Layer | Choice | Why |
|---|---|---|
| Backend | **Django 5.2 LTS** (Python 3.12/3.13) | See version note below |
| DB | **SQLite** | A presentation site has ~50 rows. Postgres adds deployment risk for zero gain |
| CSS | **Bootstrap 5.3 via CDN** + one custom `theme.css` overriding CSS variables | No Node, no build step. Deployment stays a `git pull` |
| Forms | `django-crispy-forms` + `crispy-bootstrap5` | Bootstrap-styled forms in one template tag |
| Interactivity | **HTMX** (14kb, one `<script>` tag) | Contact form submit without page reload, blog category filtering, load-more. Big perceived-quality win for near-zero effort |
| Static files | **WhiteNoise** | Serves static files from Django itself. Removes the single most common student deployment failure |
| Images | `Pillow` + `django-imagekit` (optional) | Thumbnails so the homepage isn't 8MB |
| UI-string i18n | Django built-in `gettext` + `i18n_patterns` | Already in Django, nothing to install |
| DB-content i18n | **`django-modeltranslation`** | See the gotcha in §7 — this is the one people get wrong |
| Config | `django-environ` | Keeps `SECRET_KEY` out of git |
| Icons | **Bootstrap Icons** (CDN) | Matches Bootstrap, one link tag |
| Maps | Leaflet + OpenStreetMap | Free, no API key. Google Maps needs a billing account |

> **Python version gotcha:** you have Python 3.14. Django 5.2 LTS officially supports up to 3.13; Django 6.0 supports 3.12–3.14. Either install Python 3.13 and use Django 5.2 LTS (safest, best-documented, most StackOverflow answers), or use Django 6.0 on 3.14. **I recommend Python 3.13 + Django 5.2 LTS** — fewer surprises, and the FCSE server probably won't have 3.14 either. Match your local version to whatever the server has; check this *before* writing code.

### Frontend alternatives you asked about

| Option | Verdict |
|---|---|
| **Bootstrap 5 + custom CSS variable theme** | ✅ **Do this.** The trick is not "use Bootstrap", it's "override Bootstrap so it doesn't look like Bootstrap" — see §4. Best effort-to-result ratio for this deadline |
| **Tailwind (standalone CLI binary, no Node)** | Viable if you want maximum visual control and you're already comfortable with it. Adds a build step and a compiled CSS file to commit. Prettier ceiling, slower to get there. Only pick this if you've used Tailwind before |
| **Tailwind + DaisyUI** | Nice prebuilt components, but same build-step cost. Overkill here |
| **Bulma / Pico.css** | Pico.css is genuinely great for looking clean with near-zero CSS, but it's class-light and you'll fight it the moment you need a complex layout. Not for this |
| **React / Next.js frontend + Django API** | ❌ **Don't.** Doubles the work, breaks Django's built-in i18n and server-rendered SEO, and makes FCSE deployment far harder. Server-rendered Django templates are strictly better for this assignment |
| **HTMX + Alpine.js on top of Bootstrap** | ✅ Add HTMX. Alpine only if you hit something HTMX can't do (dropdown state, image lightbox). Bootstrap's own JS already covers most of it |

**Bottom line: stick with your instinct — Django + Bootstrap. Add HTMX and a custom theme layer.**

---

## 1b. Team split (2–4 people)

Register the team and topic at the provided link — one member does it for everyone. Then split by *vertical slice*, not by layer, so nobody is blocked:

- **Person A — Core & layout:** project setup, base template, nav/footer, homepage, deployment, theme CSS
- **Person B — Content apps:** Services + detail pages, Team, About
- **Person C — Blog & contact:** Blog models/views/templates, contact form, map, cookie banner
- **Person D (if 4) — i18n, content, QA:** all translations, real copy, images, accessibility pass, link-crawler test, presentation slides

Use one Git repo, one branch per person, merge daily. Agree on the base template on **day 1** and freeze it — everyone builds inside its blocks.

---

## 2. Choose the topic (do this before anything else)

Pick an entity that naturally justifies **rich, varied content**. Weak topics make the site look thin no matter how good the code is.

**Strong picks:**

| Topic | Entity-specific elements that impress |
|---|---|
| **Restaurant / café-bakery** | Menu with categories + allergens, daily specials, table reservation form, gallery, opening hours widget that shows "Open now / Closed" |
| **Gym / fitness studio** | Weekly class schedule table, trainer profiles with specialties, membership pricing tiers, BMI calculator, class booking form |
| **Travel agency** | Destination catalog with filters, tour detail pages with itinerary, price + duration, inquiry form per tour, testimonials |
| **Auto workshop** | Service catalog with price ranges, appointment booking with date/time picker, before/after gallery, FAQ |
| **NGO / association** | Projects, events calendar, volunteer signup, donation info, annual reports, partner logos |

**Recommendation: restaurant/café-bakery or gym.** Both give you an obvious "detailed information" layer (menu item pages / class pages) and an obvious entity-specific killer feature (reservation / booking) that no generic template has.

**Fill in before starting:**

```
Entity name:        ______________
Type:               ______________
City:               ______________
Languages:          Macedonian (mk) + English (en)  [+ Albanian (sq)?]
Brand colors:       primary ______  accent ______
Killer feature:     ______________  (reservation / booking / calculator)
```

---

## 3. Information architecture

Design the sitemap first. Every page here must be reachable from the nav or a link on a parent page — the grading agent follows links.

```
/  (or /mk/, /en/)
├── Home
│     hero · services teaser (3) · about teaser · featured/menu teaser
│     · latest 3 blog posts · testimonials · CTA · map + hours
├── About
│     story · mission/values · timeline · gallery · stats counters
├── Services              → list
│   └── /services/<slug>/ → DETAIL PAGE  ← this is "detailed information"
│         full description · price · duration · gallery · FAQ · CTA
├── Team                  → list
│   └── /team/<slug>/     → DETAIL PAGE
│         bio · role · specialties · socials
├── <ENTITY-SPECIFIC>     e.g. /menu/ or /schedule/ or /tours/
│   └── detail page per item
├── Blog / News           → list, paginated, filter by category
│   └── /blog/<slug>/     → post + related posts
├── Contact
│     form · address · phone · email · hours · Leaflet map · socials
├── FAQ
├── Privacy Policy        ← required by the cookie banner
├── Terms of Use
├── 404 / 500 custom pages
├── sitemap.xml
└── robots.txt
```

**Nav rule:** max 6 top-level items. Anything more goes in a dropdown or the footer. Cluttered navs read as "unfinished" to peer reviewers.

---

## 4. Design system — the 30 peer points live here

The single highest-leverage step: **spend 45 minutes making Bootstrap not look like Bootstrap.** Everything below goes in one `static/css/theme.css` loaded *after* the Bootstrap CDN link.

### 4.1 Color

Do **not** use Bootstrap's default `#0d6efd` blue. Pick a palette that matches the entity (warm terracotta/cream for a bakery; charcoal + electric lime for a gym; deep green + sand for a travel agency).

```css
:root {
  --bs-primary: #C1440E;          /* your brand color */
  --bs-primary-rgb: 193, 68, 14;
  --brand-dark:  #1A1614;
  --brand-cream: #FAF6F0;
  --brand-accent:#E8B93F;
  --bs-body-font-family: 'Inter', system-ui, sans-serif;
  --bs-body-color: #2B2B2B;
  --bs-border-radius: 0.75rem;     /* softer than Bootstrap default */
}
.btn-primary { --bs-btn-bg: var(--bs-primary); --bs-btn-border-color: var(--bs-primary); }
```

Use a generator (coolors.co) and keep it to **2 brand colors + 1 accent + neutrals**. More than that looks amateur.

### 4.2 Typography

Two Google Fonts max — one display font for headings, one clean sans for body. This alone kills the "default template" look.

- Bakery/restaurant: `Playfair Display` + `Inter`
- Gym: `Bebas Neue` (uppercase headings) + `Inter`
- Agency/NGO: `Fraunces` + `Source Sans 3`

Preload them and set `font-display: swap` so they don't block first paint.

### 4.3 The five things that separate "polished" from "student project"

1. **Generous whitespace** — `py-5` / `py-6` between sections, never cramped
2. **Real photography** — high-quality images from Unsplash/Pexels, consistent in mood. Mismatched stock photos are the #1 tell
3. **Consistent card treatment** — pick one shadow + one radius and use it everywhere
4. **A hero that isn't a plain jumbotron** — full-bleed image with a dark gradient overlay and readable text
5. **Subtle scroll-reveal animations** — AOS library (2 CDN lines) or a 15-line IntersectionObserver. Massive perceived-quality gain

### 4.4 Non-negotiables

- Mobile-first: **test at 375px width before anything else.** A broken mobile layout costs peer points instantly
- Sticky navbar with a working hamburger
- Every image: explicit `width`/`height` (prevents layout shift), `loading="lazy"` below the fold, real `alt` text
- Consistent button hierarchy: exactly one primary CTA per section
- Contrast ratio ≥ 4.5:1 for body text

---

## 5. Data model

```python
# core
SiteSettings      # singleton: name, tagline, logo, address, phone, email, socials, map lat/lng
OpeningHours      # day_of_week, open_time, close_time, is_closed
Testimonial       # author, role, text, rating, photo, is_featured
FAQ               # question, answer, category, order

# services
ServiceCategory   # name, slug, order
Service           # title, slug, short_desc, full_desc(rich), price, duration,
                  # image, gallery(M2M), category(FK), is_featured, order
ServiceImage      # service(FK), image, caption

# team
TeamMember        # name, slug, role, bio, photo, email, linkedin,
                  # specialties(M2M), order, is_active

# blog
Category          # name, slug
Post              # title, slug, excerpt, body(rich), cover_image, author(FK),
                  # category(FK), tags, published_at, is_published, views

# contact
ContactMessage    # name, email, phone, subject, message, created_at, is_read
Reservation       # ← entity-specific: name, email, phone, date, time,
                  # party_size, notes, status(pending/confirmed/cancelled)
```

**Rules that make the teacher demo go well:**

- Every model gets `__str__`, `Meta.ordering`, `Meta.verbose_name`, and `get_absolute_url()`
- Register everything in admin with `list_display`, `list_filter`, `search_fields`, `prepopulated_fields = {'slug': ('title',)}`
- Make the admin genuinely usable — being able to say *"and the owner can edit all of this without a developer"* is worth real teacher points

---

## 6. Build order (phases)

Each phase ends in a working, committable state. Don't move forward until the current one runs.

### Phase 1 — Skeleton (Day 1)
```bash
python -m venv venv
venv\Scripts\activate
pip install django==5.2 python-dotenv django-environ pillow whitenoise django-crispy-forms crispy-bootstrap5 django-modeltranslation
django-admin startproject config .
python manage.py startapp core
```
- `config/settings/` split into `base.py`, `dev.py`, `prod.py`
- `.env` + `.gitignore` (venv, `*.sqlite3`, `.env`, `media/`, `__pycache__`)
- `requirements.txt` pinned
- WhiteNoise in middleware, `STATIC_ROOT`, `MEDIA_ROOT`
- `git init` + first commit

### Phase 2 — Base template & theme (Day 1–2)
- `templates/base.html` with blocks: `title`, `meta_description`, `extra_css`, `content`, `extra_js`
- `_navbar.html`, `_footer.html`, `_messages.html`, `_cookie_banner.html`
- Bootstrap + Bootstrap Icons + fonts + `theme.css`
- **Freeze this. Everyone else builds inside `{% block content %}`.**

### Phase 3 — Core content (Day 2–4)
- `SiteSettings` singleton + context processor so `{{ site }}` works in every template
- Home, About, Contact page views
- Custom 404/500 templates

### Phase 4 — Services + Team (Day 4–6)
- List + detail views for both, with slugs
- Detail pages must be substantive — this is the graded "detailed information"

### Phase 5 — Blog (Day 6–8)
- List with pagination (6/page), category filter, detail with related posts
- Rich text: `django-ckeditor-5` or `django-tinymce`, or plain `Textarea` + `|linebreaks` if you're short on time

### Phase 6 — Forms (Day 8–9)
- Contact form: crispy, server-side validation, honeypot field for spam, save to DB, `messages.success`, redirect (PRG pattern)
- Email via `EMAIL_BACKEND` — console backend in dev, SMTP in prod. **Wrap `send_mail` in try/except** so a mail failure never 500s the page
- Reservation/booking form (entity-specific)
- HTMX-submit the contact form so it swaps in a success message without reload

### Phase 7 — i18n (Day 9–11) — see §7
### Phase 8 — Cookies + legal (Day 11) — see §8
### Phase 9 — SEO, a11y, polish (Day 12–13) — see §9
### Phase 10 — Content & media (Day 13–14) — see §10
### Phase 11 — Deploy (Day 14–15) — see §11
### Phase 12 — QA + presentation (Day 15–16) — see §12

---

## 7. Multilingual — the part people get wrong

**The gotcha:** Django's `gettext`/`.po` files translate *template and Python strings only*. They do **not** translate database content. If your services and blog posts are in the DB, switching to English will still show Macedonian service titles — and the teacher will notice immediately.

**Solution: two mechanisms, both required.**

### 7.1 UI strings — Django built-in

```python
# settings.py
LANGUAGE_CODE = 'mk'
LANGUAGES = [('mk', 'Македонски'), ('en', 'English')]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
MIDDLEWARE = [..., 'django.middleware.locale.LocaleMiddleware', ...]  # after Session, before Common
```

```python
# urls.py
urlpatterns = i18n_patterns(
    path('', include('core.urls')),
    ...
    prefix_default_language=True,   # gives you /mk/ and /en/ — better for the crawler agent
)
```

In templates: `{% load i18n %}` then `{% trans "Contact us" %}` / `{% blocktrans %}`.
In Python: `from django.utils.translation import gettext_lazy as _`.

```bash
django-admin makemessages -l mk -l en
# edit locale/*/LC_MESSAGES/django.po
django-admin compilemessages
```

### 7.2 DB content — django-modeltranslation

```python
# services/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Service

@register(Service)
class ServiceTR(TranslationOptions):
    fields = ('title', 'short_desc', 'full_desc')
```

Add `'modeltranslation'` to `INSTALLED_APPS` **above** `django.contrib.admin`, then `makemigrations` + `migrate`. Admin now shows a tab per language, and `{{ service.title }}` automatically returns the active language.

### 7.3 Language switcher

Put it in the navbar as a small `MK | EN` toggle (or a flag dropdown). It must preserve the current page:

```django
{% load i18n %}
<form action="{% url 'set_language' %}" method="post">{% csrf_token %}
  <input name="next" type="hidden" value="{{ request.get_full_path|slice:'3:' }}">
  <button name="language" value="en" class="btn btn-sm btn-link">EN</button>
</form>
```

### 7.4 Checklist
- [ ] Every user-visible string wrapped in `{% trans %}` — including buttons, form labels, error messages, footer, alt text
- [ ] `.po` files 100% translated, `compilemessages` run
- [ ] Every translated model field filled in for both languages
- [ ] Switcher keeps you on the same page, not the homepage
- [ ] `<html lang="{{ LANGUAGE_CODE }}">`
- [ ] `<link rel="alternate" hreflang="...">` for both locales

---

## 8. Cookie consent

The assignment lists "cookies" explicitly — so it must be *visible*.

**Build it yourself** (~40 lines) rather than installing a package:

- Fixed bottom banner: short text + "Accept all" / "Only necessary" / link to Privacy Policy
- On choice: `localStorage.setItem('cookie_consent', 'all'|'necessary')` **and** set a cookie so the server knows
- Hide the banner on subsequent visits
- A small "Cookie settings" link in the footer that reopens it — this shows deliberate work
- Only load analytics *after* consent (even if you have no analytics, wire the conditional — it demos well)
- Write a real Privacy Policy page listing which cookies you set: `sessionid`, `csrftoken`, `django_language`, `cookie_consent`

Add a `{% trans %}`-wrapped version so it works in both languages.

---

## 9. SEO & accessibility — securing the 10 agent points

The automated agent "checks all pages and elements". Treat this as a hard technical checklist.

### Must pass
- [ ] **Zero 404s.** No `href="#"` placeholders anywhere. Every nav item, footer link, card, and button goes somewhere real
- [ ] Every page returns 200 in **both** `/mk/` and `/en/`
- [ ] Unique `<title>` and `<meta name="description">` per page
- [ ] Open Graph + Twitter Card tags on every page
- [ ] Semantic HTML: `<header> <nav> <main> <section> <article> <footer>` — exactly one `<main>` and one `<h1>` per page, headings in order without skipping levels
- [ ] `alt` on **every** `<img>` (empty `alt=""` only for decorative)
- [ ] Every form input has a matching `<label for>`, plus `name`, `id`, `required`, and correct `type` (`email`, `tel`, `date`)
- [ ] `aria-label` on icon-only buttons (hamburger, socials, close)
- [ ] `sitemap.xml` via `django.contrib.sitemaps`, including all detail pages in both languages
- [ ] `robots.txt`
- [ ] Favicon set + `apple-touch-icon`
- [ ] Custom 404 and 500 templates that keep the site nav
- [ ] No console errors on any page
- [ ] Keyboard navigable: visible focus rings, logical tab order, skip-to-content link
- [ ] Lighthouse ≥ 90 on Performance, Accessibility, Best Practices, SEO

### Self-test script — write this, it's the cheapest insurance

`scripts/crawl_check.py`: start from the homepage, BFS every internal link, assert every response is 200, report any `href="#"`, any `<img>` without alt, any duplicate `<title>`. Run it against the deployed URL before submitting.

```bash
pip install requests beautifulsoup4
python scripts/crawl_check.py https://your-deployed-url/
```

Also validate: [validator.w3.org](https://validator.w3.org) (HTML), WAVE browser extension (a11y).

---

## 10. Content & media

Placeholder text is the fastest way to lose peer points. Budget real time for this.

- **Copy:** write actual Macedonian + English text. No "Lorem ipsum" anywhere. AI-generate a first draft, then edit it so it sounds human and specific to your fictional business
- **Volume needed:** 6–10 services, 4–6 team members, 6–8 blog posts, 4–6 testimonials, 8–10 FAQ entries, 12–20 gallery images
- **Images:** Unsplash / Pexels / Pixabay, consistent mood and color. Resize to max 1600px wide, convert to **WebP**, keep every file under ~200KB
- **Logo:** make a simple wordmark in Figma or Canva. SVG if possible. A missing logo makes a site look unfinished from the first second
- **Fixtures:** dump seed data to `fixtures/seed.json` (`python manage.py dumpdata --indent 2`) so you can rebuild the site instantly if the deployment DB is wiped

---

## 11. Deployment on the FCSE system

**Get the official instructions from Courses first** — this section is the general shape; adapt it to what FCSE actually provides.

### Prepare for production
- `DEBUG=False`, `SECRET_KEY` from env, `ALLOWED_HOSTS = ['your.finki.ukim.mk', ...]`, `CSRF_TRUSTED_ORIGINS`
- WhiteNoise with `CompressedManifestStaticFilesStorage`
- `python manage.py collectstatic`
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` if HTTPS is available
- `python manage.py check --deploy` — fix every warning
- Media files: with `DEBUG=False` Django stops serving `/media/`. Either configure nginx for it, or add WhiteNoise's media handling, or serve user images from `static/`. **This is the #1 cause of "all my images disappeared in production."**

### Typical Linux VM deploy
```bash
git clone <repo> && cd <repo>
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py loaddata fixtures/seed.json
python manage.py createsuperuser
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```
Then a `systemd` unit for gunicorn + nginx reverse proxy. If FCSE gives you a PaaS/container instead, add a `Dockerfile` and `Procfile`.

**Deploy in week 2, not the last week.** Deploying early turns a potential disaster into a routine `git pull`. Redeploy after every phase.

### Post-deploy verification
- [ ] Homepage loads over HTTPS
- [ ] All static files and images load (check DevTools Network for 404s)
- [ ] Contact form submits and the message appears in admin
- [ ] Both languages work on the live URL
- [ ] Admin is reachable and the superuser can log in
- [ ] `crawl_check.py` passes against the live URL
- [ ] Works on a real phone, not just DevTools

---

## 12. Peer review, presentation, and the other 40 points

### The 10 easy points — reviewing others
Do all 3 assigned reviews. For each, write 4–6 sentences covering: what works, what's missing versus the required elements, a specific technical observation (mobile, load time, a broken link), and a justification for the 0–5 score. Vague one-liners risk the points; specific feedback guarantees them.

### The 30 points — being reviewed
Reviewers see your site for ~3 minutes on whatever device they have. Optimize for that:
- Loads in under 2 seconds
- Homepage tells them what the business is within 3 seconds
- Nothing broken, nothing placeholder, no console errors
- Flawless on mobile
- Ask a friend outside the team to click through and tell you what looks unfinished

### The 50 points — the teacher presentation
Prepare a **10-minute demo script**:
1. The entity and why you chose it (30s)
2. Live walkthrough hitting **every required element by name** — say "here is the multilingual support", "here is the cookie consent" out loud so nothing gets missed (4 min)
3. The admin panel — show the owner can edit content without a developer (2 min)
4. Your entity-specific feature, end to end: submit a reservation → show it appear in admin (2 min)
5. Architecture in one slide: apps, models, i18n approach, deployment (1 min)
6. Q&A (30s)

Rehearse it once with a timer. Have a **local copy running as a backup** in case the deployed site or the venue Wi-Fi fails.

---

## 13. Timeline

Today is **31 July 2026**; the deadline is in **September**. That's comfortable — but front-load it.

| Week | Focus | Done when |
|---|---|---|
| **1** (Aug 1–7) | Topic locked, team registered, repo up, Phases 1–3 | Base template frozen, homepage renders with real theme |
| **2** (Aug 8–14) | Phases 4–6, **first deployment** | Services/Team/Blog/Contact all live on the FCSE URL |
| **3** (Aug 15–21) | Phases 7–8, entity-specific feature | Both languages fully working, cookie banner live |
| **4** (Aug 22–28) | Phases 9–10, real content and images | No placeholders anywhere, Lighthouse ≥ 90 |
| **5** (Aug 29–Sep 4) | QA, crawl check, fix everything | `crawl_check.py` green, tested on real phones |
| **6** (Sep) | Submit link, do 3 peer reviews, rehearse demo | Submitted, reviews written, presentation timed |

**Compressed version if you're short on time (10 days):** Phases 1–2 (day 1–2), 3–5 (day 3–5), 6 + deploy (day 6), 7–8 (day 7–8), 9–10 (day 9), QA (day 10). Cut: the blog rich-text editor (plain textarea), image thumbnails, scroll animations. **Never cut:** multilingual, cookie banner, contact form, real content, deployment.

---

## 14. Common failure modes

| Trap | Fix |
|---|---|
| Deploying in the last 48 hours | Deploy in week 2, redeploy every phase |
| DB content stays in one language | `django-modeltranslation` from the start (§7.2) |
| Images vanish with `DEBUG=False` | Configure media serving explicitly (§11) |
| `href="#"` left in the nav | The crawl check catches these — run it |
| Site looks like stock Bootstrap | Custom color + font layer, day 1 (§4) |
| Lorem ipsum in the final build | Grep for "lorem", "placeholder", "TODO" before submitting |
| Contact form 500s because SMTP fails | Wrap `send_mail` in try/except; always save to DB first |
| Mobile layout broken | Test at 375px continuously, not at the end |
| Forgetting to review 3 projects | Calendar reminder. It's 10 free points |
| Repo has `SECRET_KEY` committed | `.env` + `.gitignore` from commit #1 |

---

## 15. Prompt template — how to hand this to Claude

Use one prompt per phase. Small scoped prompts produce far better code than one giant "build the whole site" request.

### Kickoff prompt

```
I'm building a Django + Bootstrap 5 presentation website for my Business Practice
course at FCSE. Follow PROJECT_PLAN.md in this directory as the spec.

Context:
- Entity: <NAME>, a <TYPE> in <CITY>
- Languages: Macedonian (default) + English
- Brand: primary <#HEX>, accent <#HEX>, fonts <DISPLAY> + <BODY>
- Killer feature: <reservation / booking / calculator>
- Python <VERSION>, Django <VERSION>, SQLite, Bootstrap 5.3 via CDN, HTMX, WhiteNoise

Start with Phase 1 (skeleton) and Phase 2 (base template + theme) from the plan.
Set up the project structure, split settings, .env, .gitignore, requirements.txt,
and build base.html with navbar, footer, cookie banner placeholder, and theme.css
implementing the brand colors and fonts.

Do not scaffold apps beyond `core` yet. Show me the running homepage before moving on.
```

### Per-phase prompt

```
Continue with Phase <N> (<name>) from PROJECT_PLAN.md.
Reuse the existing base template and theme — do not change base.html.
Include: models with __str__/Meta/get_absolute_url, admin registration with
list_display/list_filter/search_fields/prepopulated_fields, views, urls, templates,
and all user-facing strings wrapped in {% trans %}.
Register translated fields with modeltranslation where the content is user-visible.
```

### Review prompt (run before submission)

```
Audit this project against §9 of PROJECT_PLAN.md (SEO & accessibility checklist).
Check every template for: missing alt text, missing form labels, href="#" placeholders,
heading level skips, missing meta tags, and untranslated strings.
Then write scripts/crawl_check.py as described in §9 and run it against
http://127.0.0.1:8000/. Report findings as a prioritized list.
```

---

## Next actions

1. Lock the topic and fill in the blanks in §2
2. Register the team + topic at the assignment link
3. Confirm the Python/Django version available on the FCSE server
4. Pull the FCSE deployment instructions from Courses
5. Run the kickoff prompt in §15
