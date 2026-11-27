"""Checks that every vendored file a template loads is produced by `npm run vendor`."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "app" / "templates"
STATIC = ROOT / "app" / "static"
VENDOR = STATIC / "vendor"

VENDOR_REF = re.compile(r"url_for\(\s*'static',\s*filename='(vendor/[^']+)'\s*\)")


def vendor_refs():
    refs = set()
    for template in TEMPLATES.rglob("*.html"):
        refs.update(VENDOR_REF.findall(template.read_text(encoding="utf-8")))
    return sorted(refs)


def test_templates_reference_vendored_assets():
    assert vendor_refs(), "expected templates to load libraries from static/vendor"


@pytest.mark.parametrize("ref", vendor_refs())
def test_vendored_asset_exists(ref):
    if not VENDOR.is_dir():
        pytest.fail("app/static/vendor/ is missing, run `npm ci && npm run vendor`")
    assert (STATIC / ref).exists(), f"{ref} is not produced by scripts/vendor.mjs"


def test_three_addons_resolve():
    """Addons are imported through the "three/addons/" import map prefix."""
    if not VENDOR.is_dir():
        pytest.fail("app/static/vendor/ is missing, run `npm ci && npm run vendor`")
    imports = set()
    sources = [*(STATIC / "js").glob("*.js"), *TEMPLATES.rglob("*.html")]
    for source in sources:
        imports.update(
            re.findall(r"from\s+[\"']three/addons/([^\"']+)[\"']", source.read_text())
        )
    assert imports
    for addon in sorted(imports):
        assert (VENDOR / "three" / "addons" / addon).exists(), (
            f"three/addons/{addon} is imported but not vendored, "
            "add it to THREE_ADDONS in scripts/vendor.mjs"
        )
