import io
import os
from datetime import date, timedelta

import pytest

from app import events_store
from app.db import db
from app.models import Event, User

PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01"
    b"\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.fixture
def clean(app):
    def wipe():
        with app.app_context():
            db.create_all(bind_key="users")
            db.session.execute(db.delete(Event))
            db.session.execute(
                db.delete(User).where(
                    User.username.in_(["events-admin", "events-member"])
                )
            )
            db.session.commit()

    wipe()
    yield
    wipe()


def add_event(app, name, start, end=None, **fields):
    with app.app_context():
        event = Event(name=name, start_date=start, end_date=end, **fields)
        db.session.add(event)
        db.session.commit()
        return event.id


def sign_in(app, client, admin):
    with app.app_context():
        user = User(
            name="Events Admin",
            username="events-admin" if admin else "events-member",
            branch="CS",
            mobile_no="",
            password="x",
            is_admin=admin,
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    with client.session_transaction() as session:
        session["_user_id"] = str(user_id)
        session["_fresh"] = True
        session["_csrf_token"] = "test-token"


@pytest.mark.parametrize(
    "text, start, end",
    [
        ("October 24, 2026", date(2026, 10, 24), None),
        ("October 24 - 25, 2026", date(2026, 10, 24), date(2026, 10, 25)),
        ("September 29 - October 1, 2026", date(2026, 9, 29), date(2026, 10, 1)),
        ("September 09, 2026", date(2026, 9, 9), None),
        ("Oct 4th, 2024", date(2024, 10, 4), None),
        ("Oct 4th - Oct 5th, 2024", date(2024, 10, 4), date(2024, 10, 5)),
        ("October 21, 2024 - October 25, 2024", date(2024, 10, 21), date(2024, 10, 25)),
    ],
)
def test_old_date_strings_parse(text, start, end):
    assert events_store.parse_date_label(text) == (start, end)


def test_date_labels():
    label = events_store.date_label
    assert label(date(2026, 10, 24)) == "October 24, 2026"
    assert label(date(2026, 10, 24), date(2026, 10, 25)) == "October 24 - 25, 2026"
    assert (
        label(date(2026, 9, 29), date(2026, 10, 1)) == "September 29 - October 1, 2026"
    )
    assert (
        label(date(2026, 12, 30), date(2027, 1, 2))
        == "December 30, 2026 - January 2, 2027"
    )


def test_every_seed_event_imports_once(app, clean):
    from app.data.events_seed import events as seed

    with app.app_context():
        added, skipped = events_store.import_events(seed)
        assert (added, skipped) == (len(seed), 0)
        assert events_store.import_events(seed) == (0, len(seed))
        stored = events_store.all_events()
    assert [e["name"] for e in stored][:1] and len(stored) == len(seed)
    assert all(
        not e["image_url"] or e["image_url"].startswith(("/", "http")) for e in stored
    )


def test_pages_read_events_from_the_database(app, client, clean):
    soon = date.today() + timedelta(days=10)
    add_event(app, "Future Hack", soon, description="Coming up", topics_text="One\nTwo")
    add_event(app, "Old Talk", date(2020, 1, 5))

    events_page = client.get("/events").data
    assert b"Future Hack" in events_page and b"Old Talk" in events_page

    detail = client.get("/events/Future Hack")
    assert detail.status_code == 200
    assert b"<li>One</li>" in detail.data and b"<li>Two</li>" in detail.data

    assert client.get("/events/Nope").status_code == 200  # the friendly not found page

    with app.app_context():
        events = events_store.all_events()
    assert [e["name"] for e in events] == ["Future Hack", "Old Talk"]
    assert events_store.is_upcoming(events[0]) and not events_store.is_upcoming(
        events[1]
    )


def test_a_multi_day_event_stays_upcoming_until_its_last_day(app, clean):
    add_event(app, "Fest", date.today() - timedelta(days=1), date.today())
    with app.app_context():
        (fest,) = events_store.all_events()
    assert events_store.is_upcoming(fest)


def test_manage_pages_are_admin_only(app, client, clean):
    assert client.get("/events/admin/manage").status_code in (302, 401, 403)
    sign_in(app, client, admin=False)
    assert client.get("/events/admin/manage").status_code == 403


def test_admin_adds_an_event_with_an_uploaded_image(app, client, clean):
    sign_in(app, client, admin=True)
    resp = client.post(
        "/events/admin/manage/new",
        data={
            "csrf_token": "test-token",
            "name": "  Robo   Night ",
            "start_date": "2026-12-05",
            "end_date": "2026-12-06",
            "description": "Robots.",
            "topics": "Line one\n\n Line two ",
            "moredetails": "https://example.com/more",
            "image": (io.BytesIO(PNG), "robot.png"),
        },
        content_type="multipart/form-data",
    )
    assert resp.status_code == 302
    with app.app_context():
        event = db.session.scalars(db.select(Event)).one()
        assert event.name == "Robo Night"
        assert event.end_date == date(2026, 12, 6)
        assert event.topics == ["Line one", "Line two"]
        assert event.image_url.startswith("/static/uploads/events/")
        path = os.path.join(app.root_path, event.image_url.lstrip("/"))
    assert os.path.exists(path)
    os.remove(path)


def test_admin_edits_and_deletes(app, client, clean):
    event_id = add_event(app, "Draft", date(2026, 1, 1))
    sign_in(app, client, admin=True)
    assert b"Draft" in client.get("/events/admin/manage").data

    client.post(
        f"/events/admin/manage/{event_id}",
        data={
            "csrf_token": "test-token",
            "name": "Final",
            "start_date": "2026-01-02",
            "end_date": "2026-01-02",
            "image_url": "/static/img/x.png",
        },
    )
    with app.app_context():
        event = db.session.get(Event, event_id)
        assert (event.name, event.start_date, event.end_date) == (
            "Final",
            date(2026, 1, 2),
            None,
        )
        assert event.image_url == "/static/img/x.png"

    client.post(
        f"/events/admin/manage/{event_id}/delete", data={"csrf_token": "test-token"}
    )
    with app.app_context():
        assert db.session.get(Event, event_id) is None


@pytest.mark.parametrize(
    "fields, message",
    [
        ({"name": "", "start_date": "2026-01-01"}, b"Name is required"),
        ({"name": "A/B", "start_date": "2026-01-01"}, b"cannot contain a slash"),
        ({"name": "X", "start_date": ""}, b"Start date is required"),
        (
            {"name": "X", "start_date": "2026-01-02", "end_date": "2026-01-01"},
            b"End date cannot be before",
        ),
        (
            {
                "name": "X",
                "start_date": "2026-01-01",
                "moredetails": "javascript:alert(1)",
            },
            b"full link",
        ),
    ],
)
def test_bad_input_is_refused_and_kept_in_the_form(app, client, clean, fields, message):
    sign_in(app, client, admin=True)
    resp = client.post(
        "/events/admin/manage/new", data={"csrf_token": "test-token", **fields}
    )
    assert resp.status_code == 200
    assert message in resp.data
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(Event)) == 0


def test_duplicate_names_are_refused(app, client, clean):
    add_event(app, "Taken", date(2026, 1, 1))
    sign_in(app, client, admin=True)
    resp = client.post(
        "/events/admin/manage/new",
        data={"csrf_token": "test-token", "name": "Taken", "start_date": "2026-02-01"},
    )
    assert b"already exists" in resp.data


def test_changes_need_the_csrf_token(app, client, clean):
    event_id = add_event(app, "Keep", date(2026, 1, 1))
    sign_in(app, client, admin=True)
    assert client.post(f"/events/admin/manage/{event_id}/delete").status_code == 400
    assert (
        client.post(
            "/events/admin/manage/new",
            data={"csrf_token": "wrong", "name": "X", "start_date": "2026-01-01"},
        ).status_code
        == 400
    )
    with app.app_context():
        assert db.session.get(Event, event_id) is not None
