"""Events, read from the database.

Pages get plain dicts with the same keys the old `app/data/events.py` list had
(`name`, `date`, `slug`, `topics`, ...), so templates did not need to change.
"""

import re
import urllib.parse
from datetime import date

from app.db import db
from app.models import Event

MONTHS = {
    name.lower(): number
    for number, names in enumerate(
        [
            ("January", "Jan"),
            ("February", "Feb"),
            ("March", "Mar"),
            ("April", "Apr"),
            ("May",),
            ("June", "Jun"),
            ("July", "Jul"),
            ("August", "Aug"),
            ("September", "Sep", "Sept"),
            ("October", "Oct"),
            ("November", "Nov"),
            ("December", "Dec"),
        ],
        start=1,
    )
    for name in names
}


def date_label(start, end=None):
    """`October 24, 2026`, `October 24 - 25, 2026`, `September 29 - October 1,
    2026`, or across years `December 30, 2026 - January 2, 2027`."""
    if not end or end == start:
        return f"{start:%B} {start.day}, {start.year}"
    if start.year != end.year:
        return f"{start:%B} {start.day}, {start.year} - {end:%B} {end.day}, {end.year}"
    if start.month != end.month:
        return f"{start:%B} {start.day} - {end:%B} {end.day}, {end.year}"
    return f"{start:%B} {start.day} - {end.day}, {end.year}"


_PART = re.compile(r"^([A-Za-z]+)?\s*(\d{1,2})(?:st|nd|rd|th)?(?:,\s*(\d{4}))?$")


def parse_date_label(text):
    """Reads the date strings the old events list used, including forms like
    `Oct 4th - Oct 5th, 2024` and `October 21, 2024 - October 25, 2024`.
    Returns (start, end), with end None for a single day."""
    text = text.strip()
    year_match = re.search(r",?\s*(\d{4})$", text)
    if not year_match:
        raise ValueError(f"no year in date {text!r}")
    year = int(year_match.group(1))
    parts = [p.strip() for p in text[: year_match.start()].split(" - ")]
    if len(parts) > 2:
        raise ValueError(f"unexpected date {text!r}")

    parsed, month = [], None
    for part in parts:
        match = _PART.match(part)
        if not match:
            raise ValueError(f"unexpected date {text!r}")
        month_name, day, part_year = match.groups()
        if month_name:
            month = MONTHS.get(month_name.lower())
            if month is None:
                raise ValueError(f"unknown month in {text!r}")
        if month is None:
            raise ValueError(f"no month in {text!r}")
        parsed.append(date(int(part_year) if part_year else year, month, int(day)))

    start = parsed[0]
    end = parsed[1] if len(parsed) == 2 else None
    if end and end < start:
        raise ValueError(f"end before start in {text!r}")
    return start, (end if end != start else None)


def slug(name):
    return urllib.parse.quote(name.encode("utf-8"))


def to_dict(event):
    return {
        "id": event.id,
        "name": event.name,
        "slug": slug(event.name),
        "description": event.description,
        "date": date_label(event.start_date, event.end_date),
        "start_date": event.start_date,
        "end_date": event.end_date or event.start_date,
        "image_url": event.image_url,
        "moredetails": event.moredetails,
        "registration_link": event.registration_link,
        "instagram_link": event.instagram_link,
        "facebook_link": event.facebook_link,
        "topics": event.topics,
    }


def all_events():
    """Newest first, the order the pages have always used."""
    rows = db.session.scalars(
        db.select(Event).order_by(Event.start_date.desc(), Event.id.desc())
    ).all()
    return [to_dict(e) for e in rows]


def find_by_name(name):
    event = db.session.scalars(db.select(Event).filter_by(name=name)).first()
    return to_dict(event) if event else None


def is_upcoming(event, today=None):
    """Still upcoming until its last day has passed."""
    return event["end_date"] >= (today or date.today())


def _link(value):
    """Old entries sometimes wrote `static/...`, which only worked on pages at
    the site root; make those site paths."""
    value = (value or "").strip()
    if value and not value.startswith(("http://", "https://", "/")):
        value = "/" + value
    return value


def import_events(items):
    """Adds events from the old list format, skipping names already present.
    Returns (added, skipped)."""
    existing = set(db.session.scalars(db.select(Event.name)).all())
    added = skipped = 0
    for item in items:
        name = item["name"].strip()
        if name in existing:
            skipped += 1
            continue
        start, end = parse_date_label(item["date"])
        db.session.add(
            Event(
                name=name,
                description=item.get("description") or "",
                start_date=start,
                end_date=end,
                image_url=_link(item.get("image_url")),
                moredetails=_link(item.get("moredetails")),
                registration_link=_link(item.get("registration_link")),
                instagram_link=_link(item.get("instagram_link")),
                facebook_link=_link(item.get("facebook_link")),
                topics_text="\n".join(item.get("topics") or []),
            )
        )
        existing.add(name)
        added += 1
    db.session.commit()
    return added, skipped
