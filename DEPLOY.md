# Deployment guide — FORGE Fitness Studio

> **Before anything else: get the official FCSE deployment instructions from Courses.**
> This guide covers the general shape of a Django deployment. Adapt the server-specific
> parts (paths, service manager, domain) to whatever FCSE actually provides.

---

## 0. What you need from FCSE

Find these out first — they determine everything below:

- [ ] Hostname / URL you have been assigned
- [ ] SSH access details, or the upload method
- [ ] Python version available on the server (**must be 3.10–3.13** for Django 5.2)
- [ ] Whether HTTPS is available
- [ ] Whether there is an nginx/Apache in front, or whether you serve directly
- [ ] Whether you may run a long-lived process (gunicorn + systemd) or only WSGI/passenger

---

## 1. Local pre-flight

Run all four. Do not deploy until every one is green.

```bash
venv\Scripts\python.exe manage.py test
```

```bash
venv\Scripts\python.exe scripts\crawl_check.py
```

```bash
venv\Scripts\python.exe scripts\i18n_tools.py compile
```

```bash
venv\Scripts\python.exe manage.py check --deploy
```

---

## 2. Get the code onto the server

```bash
git clone <your-repo-url> forge
cd forge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt
```

`requirements-prod.txt` includes gunicorn; `requirements.txt` alone does not, because
gunicorn cannot run on Windows and installing it locally just produces a confusing error.

---

## 3. Create the production `.env`

**Never copy your local `.env`** — it has `DEBUG=True` and a key that has been on your laptop.

```bash
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
nano .env
```

Minimum production values:

```ini
DEBUG=False
SECRET_KEY=<the freshly generated key>
ALLOWED_HOSTS=your.finki.ukim.mk
CSRF_TRUSTED_ORIGINS=https://your.finki.ukim.mk

# Set to False if FCSE serves over plain HTTP — otherwise SECURE_SSL_REDIRECT
# causes an infinite redirect loop and the site appears completely broken.
HTTPS_ENABLED=True
```

> `ALLOWED_HOSTS` must contain the real hostname or every request returns
> **400 Bad Request**. This is the most common first-deploy failure.

---

## 4. Build and populate

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_demo
python manage.py createsuperuser
```

Translations: the repo commits `.po` files but not compiled `.mo` (they are gitignored,
since they are build artefacts). Compile them on the server:

```bash
python scripts/i18n_tools.py compile
```

If GNU gettext is installed on the server you can use Django's own command instead —
they produce the same result:

```bash
python manage.py compilemessages
```

**Without this step the entire site renders in English**, because Macedonian is the
default language and its catalogue would be missing.

---

## 5. Run it

### Option A — gunicorn behind nginx (preferred)

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

`config/wsgi.py` already defaults to `config.settings.prod`, so no extra environment
variable is needed.

systemd unit at `/etc/systemd/system/forge.service`:

```ini
[Unit]
Description=FORGE Fitness Studio
After=network.target

[Service]
User=<your-user>
WorkingDirectory=/home/<your-user>/forge
EnvironmentFile=/home/<your-user>/forge/.env
ExecStart=/home/<your-user>/forge/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now forge && sudo systemctl status forge
```

nginx site config:

```nginx
server {
    listen 80;
    server_name your.finki.ukim.mk;
    client_max_body_size 10M;

    location /static/ { alias /home/<your-user>/forge/staticfiles/; expires 30d; }
    location /media/  { alias /home/<your-user>/forge/media/; expires 7d; }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

`X-Forwarded-Proto` matters: `prod.py` sets `SECURE_PROXY_SSL_HEADER` to read it, and
without it Django thinks every HTTPS request is HTTP and redirect-loops.

### Option B — no web server in front

Works with no extra configuration. WhiteNoise serves both static **and** media files —
see `config/whitenoise_media.py`. Just run gunicorn bound to the public port.

---

## 6. Media files — read this even if you skip everything else

With `DEBUG=False`, Django stops serving `MEDIA_URL`. Every photo uploaded through the
admin then 404s, and the site looks broken. This project handles it in two ways:

- **With nginx** — the `location /media/` block above serves them. Fastest option.
- **Without nginx** — `WhiteNoiseMediaMiddleware` in `config/whitenoise_media.py`
  serves `MEDIA_ROOT`. `prod.py` also sets `WHITENOISE_AUTOREFRESH = True` so newly
  uploaded photos appear without restarting the process.

Also make sure `media/` exists and is writable by the process user:

```bash
mkdir -p media && chmod u+rwX media
```

---

## 7. Post-deploy verification

Run the crawler against the live site — this is the check that protects the 10 automated
grading points:

```bash
python scripts/crawl_check.py https://your.finki.ukim.mk
```

Then confirm by hand:

- [ ] Homepage loads over HTTPS with no mixed-content warnings
- [ ] CSS and images load (DevTools → Network → no 404s)
- [ ] `/mk/` **and** `/en/` both work, and the language switcher stays on the same page
- [ ] Macedonian actually renders in Macedonian (if not, `.mo` files were not compiled)
- [ ] Contact form submits and the message appears in `/admin/`
- [ ] Booking form submits and appears in `/admin/`
- [ ] Cookie banner appears once, and stays dismissed after reload
- [ ] `/sitemap.xml` and `/robots.txt` load
- [ ] A deliberate 404 (e.g. `/mk/nonsense/`) shows the styled error page
- [ ] Admin login works
- [ ] Open it on a real phone, not just DevTools

---

## 8. Redeploying after a change

```bash
cd forge && git pull
source venv/bin/activate
pip install -r requirements-prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
python scripts/i18n_tools.py compile
sudo systemctl restart forge
```

---

## 9. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| 400 Bad Request on every page | Hostname missing from `ALLOWED_HOSTS` | Add the real hostname to `.env` |
| Infinite redirect loop | `SECURE_SSL_REDIRECT` on, but site is HTTP | Set `HTTPS_ENABLED=False` in `.env` |
| Site loads but has no styling | `collectstatic` not run, or wrong `STATIC_ROOT` | Re-run `collectstatic` |
| All uploaded photos 404 | Media not served with `DEBUG=False` | See §6 |
| Whole site is in English | `.mo` files not compiled | `python scripts/i18n_tools.py compile` |
| `CSRF verification failed` on forms | `CSRF_TRUSTED_ORIGINS` missing the scheme | Use the full `https://host` form |
| 500 with no detail | Correct — `DEBUG=False` hides it | `sudo journalctl -u forge -n 50` |
| `collectstatic` fails on a missing file | CSS references a file that isn't there | Fix the reference; don't downgrade the storage backend |
