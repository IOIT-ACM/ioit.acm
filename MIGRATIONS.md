# Manual DB Migrations — Event Notification Feature (Issue #54)

This project does not use a migration framework (no Flask-Migrate/Alembic, no `migrations/` directory). Tables are created via `db.create_all(bind=None)` in `app/__init__.py`, which only creates **new** tables — it will **not** alter existing tables. Any change to an already-existing table (like adding a column to `users`) must be applied manually on every environment (local, staging, production).

This file tracks those manual steps for the event notification feature so they aren't lost before deployment.

All new tables/columns use the `"users"` bind key (same MySQL database as the `users` table), since `EmailLog.sent_by_user_id` has a foreign key into `users.id`.

---

## 1. Add `is_admin` column to existing `users` table

New tables get created automatically by `db.create_all()`, but this is an **existing** table, so it needs a manual `ALTER TABLE`.

```sql
ALTER TABLE users
ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE;
```

**Run this manually on every environment** (local dev DB, staging, production) before deploying code that references `User.is_admin`. Deploying the code without this step will cause errors on any query touching the `users` table.

A helper script `scripts/set_admin.py` is provided to check for/apply this column automatically on local setups — see below.

---

## 2. New tables: `subscribers` and `email_logs`

These are brand new tables, so they **will** be created automatically the next time the app starts and `db.create_all(bind=None)` runs (as long as the corresponding models are defined in `models.py`). No manual SQL is required for these two — listed here only for completeness/audit purposes.

```sql
-- subscribers (auto-created via db.create_all(), shown here for reference only)
CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- email_logs (auto-created via db.create_all(), shown here for reference only)
CREATE TABLE email_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    template_used VARCHAR(100),
    event_slugs TEXT,
    body_snapshot TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sent_by_user_id INT NOT NULL,
    recipient_count INT NOT NULL DEFAULT 0,
    FOREIGN KEY (sent_by_user_id) REFERENCES users(id)
);
```

---

## 3. Deployment checklist

Before this feature goes live on any environment:

- [ ] Run the `is_admin` `ALTER TABLE` statement (Section 1) manually against that environment's `users` table.
- [ ] Confirm `subscribers` and `email_logs` tables exist (they should auto-create on next app start via `db.create_all()` — verify with a quick `SHOW TABLES;` or DB browser check rather than assuming).
- [ ] Run `scripts/set_admin.py <username>` to flag at least one real team member as admin on that environment (there is no self-serve way to become admin — this is intentional).
- [ ] Confirm mail environment variables are set for that environment (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`) — using **real** `events@ioit.acm.org` SMTP credentials in staging/production, not the local Mailpit values used during development.

---

## Notes

- If this project adopts a real migration tool (Flask-Migrate/Alembic) in the future, these manual steps should be converted into a proper migration file at that time, and this document can be retired.
- Local development should use Mailpit (or Maildev) for mail testing — see the feature task spec for setup — so no real subscriber emails are sent accidentally during development.
