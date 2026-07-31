"""Makes site-wide data available to every template without repeating it in
every view. Registered in TEMPLATES['OPTIONS']['context_processors']."""

from datetime import datetime

from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone

from .models import OpeningHours, SiteSettings


def _is_open_now(hours_by_day):
    now = timezone.localtime()
    today = hours_by_day.get(now.weekday())
    if not today or today.is_closed or not today.opens or not today.closes:
        return False
    current = now.time()
    if today.closes <= today.opens:  # spans midnight
        return current >= today.opens or current < today.closes
    return today.opens <= current < today.closes


def site_settings(request):
    """Provides {{ site }}, {{ opening_hours }} and {{ is_open_now }} everywhere.

    Wrapped in try/except so `migrate` and `collectstatic` still work on a fresh
    checkout where the tables do not exist yet.
    """
    try:
        site = SiteSettings.load()
        hours = list(OpeningHours.objects.all())
    except (OperationalError, ProgrammingError):
        return {"site": None, "opening_hours": [], "is_open_now": False}

    return {
        "site": site,
        "opening_hours": hours,
        "is_open_now": _is_open_now({h.weekday: h for h in hours}),
        "current_year": datetime.now().year,
    }
