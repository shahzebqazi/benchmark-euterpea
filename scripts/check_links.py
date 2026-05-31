#!/usr/bin/env python3
"""Check generated site internal links."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_DIR = REPO_ROOT / "docs" / "site" / "dist"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link", "script", "img"}:
            return
        attr_name = "href" if tag in {"a", "link"} else "src"
        for name, value in attrs:
            if name == attr_name and value:
                self.links.append(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check internal links in generated site HTML.")
    parser.add_argument("--site-dir", type=Path, default=DEFAULT_SITE_DIR)
    return parser.parse_args()


def is_external(link: str) -> bool:
    parsed = urlparse(link)
    return bool(parsed.scheme or parsed.netloc or link.startswith("mailto:"))


def check_site(site_dir: Path) -> list[str]:
    if not site_dir.is_dir():
        return [f"missing site directory: {site_dir}"]

    errors: list[str] = []
    for html_path in sorted(site_dir.glob("*.html")):
        parser = LinkParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for raw_link in parser.links:
            link, _fragment = urldefrag(raw_link)
            if not link or is_external(link):
                continue
            target = (html_path.parent / link).resolve()
            try:
                target.relative_to(site_dir.resolve())
            except ValueError:
                errors.append(f"{html_path.relative_to(site_dir)} links outside site: {raw_link}")
                continue
            if not target.exists():
                errors.append(f"{html_path.relative_to(site_dir)} has broken link: {raw_link}")
    return errors


def main() -> int:
    args = parse_args()
    errors = check_site(args.site_dir.resolve())
    if errors:
        for error in errors:
            print(f"error: {error}")
        return 1
    print(f"checked internal links in {args.site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
