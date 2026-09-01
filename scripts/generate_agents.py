#!/usr/bin/env python3
"""Generate a selected, repository-specific AGENTS.md from modular guides."""

from __future__ import annotations

import argparse
import curses
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

CATEGORY_ORDER = ("header", "structure", "process", "testing", "observability", "language")
VALID_CATEGORIES = set(CATEGORY_ORDER)
VERSION = "1"
FrontMatterValue: TypeAlias = str | list[str]


@dataclass(frozen=True)
class Guide:
    id: str
    title: str
    summary: str
    category: str
    language: str | None
    requires: tuple[str, ...]
    section: str | None
    section_title: str | None
    body: str
    path: Path


def parse_front_matter(path: Path) -> Guide:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML front matter")
    _, front_matter, body = text.split("---\n", 2)
    data: dict[str, FrontMatterValue] = {}
    current_list: str | None = None
    for line in front_matter.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list:
            values = data.get(current_list)
            if not isinstance(values, list):
                raise ValueError(f"{path}: list item without a list field")
            values.append(line[4:].strip())
            continue
        match = re.fullmatch(r"([a-z_]+):(?:\s*(.*))?", line)
        if not match:
            raise ValueError(f"{path}: unsupported front matter line: {line!r}")
        key, value = match.groups()
        current_list = key if value == "" else None
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            data[key] = value
    required = [
        field for field in ("id", "title", "summary", "category") if not isinstance(data.get(field), str)
    ]
    if required:
        raise ValueError(f"{path}: missing required metadata: {', '.join(required)}")
    identifier, category = data["id"], data["category"]
    assert isinstance(identifier, str)
    assert isinstance(category, str)
    if not re.fullmatch(r"[a-z][a-z0-9-]*", identifier):
        raise ValueError(f"{path}: id must be kebab-case")
    if category not in VALID_CATEGORIES:
        raise ValueError(f"{path}: invalid category {category!r}")
    language = data.get("language")
    if language is not None and not isinstance(language, str):
        raise ValueError(f"{path}: language must be a string")
    if category == "language" and not language:
        raise ValueError(f"{path}: language guides require language metadata")
    requires = data.get("requires", [])
    if not isinstance(requires, list) or not all(isinstance(item, str) for item in requires):
        raise ValueError(f"{path}: requires must be a list of guide IDs")
    title, summary = data["title"], data["summary"]
    assert isinstance(title, str)
    assert isinstance(summary, str)
    section, section_title = data.get("section"), data.get("section_title")
    if section is not None and not isinstance(section, str):
        raise ValueError(f"{path}: section must be a string")
    if section_title is not None and not isinstance(section_title, str):
        raise ValueError(f"{path}: section_title must be a string")
    return Guide(identifier, title, summary, category, language, tuple(requires), section, section_title,
                 body.strip(), path)


def discover_guides(root: Path, output: Path) -> dict[str, Guide]:
    guides: dict[str, Guide] = {}
    for path in root.rglob("AGENTS*.md"):
        if (
            any(part.startswith(".") for part in path.relative_to(root).parts)
            or path.name == "AGENTS.md"
            or path.resolve() == output.resolve()
        ):
            continue
        guide = parse_front_matter(path)
        if guide.id in guides:
            raise ValueError(f"duplicate guide id {guide.id!r}: {guides[guide.id].path} and {path}")
        guides[guide.id] = guide
    if not guides:
        raise ValueError(f"no AGENTS*.md guides found below {root}")
    headers = [guide for guide in guides.values() if guide.category == "header"]
    if len(headers) > 1:
        raise ValueError("only one header guide is allowed")
    missing = sorted({required for guide in guides.values() for required in guide.requires} - guides.keys())
    if missing:
        raise ValueError(f"unknown required guide IDs: {', '.join(missing)}")
    sections = {}
    for guide in guides.values():
        if guide.section:
            if not guide.section_title:
                raise ValueError(f"{guide.path}: section requires section_title")
            if sections.setdefault(guide.section, guide.section_title) != guide.section_title:
                raise ValueError(f"conflicting titles for section {guide.section!r}")
    return guides


def resolve_selection(guides: dict[str, Guide], selected: list[str]) -> list[Guide]:
    unknown = sorted(set(selected) - guides.keys())
    if unknown:
        raise ValueError(f"unknown guide IDs: {', '.join(unknown)}")
    resolved: set[str] = set()

    def add(dependency_id: str) -> None:
        if dependency_id not in resolved:
            resolved.add(dependency_id)
            for required in guides[dependency_id].requires:
                add(required)

    for selected_id in selected:
        add(selected_id)
    resolved.update(guide.id for guide in guides.values() if guide.category == "header")
    positions = {category: index for index, category in enumerate(CATEGORY_ORDER)}
    return sorted((guides[resolved_id] for resolved_id in resolved),
                  key=lambda guide: (positions[guide.category], guide.title.lower(), guide.id))


def dependents(guides: dict[str, Guide], selected: set[str], identifier: str) -> set[str]:
    removed = {identifier}
    changed = True
    while changed:
        changed = False
        for guide in guides.values():
            if guide.id in selected and guide.id not in removed and any(
                requirement in removed for requirement in guide.requires
            ):
                removed.add(guide.id)
                changed = True
    return removed


def choose_interactively(guides: dict[str, Guide]) -> list[str]:
    categories = [category for category in CATEGORY_ORDER if category != "header"]
    required_categories = {"structure", "process"}
    choices = {
        category: sorted((guide for guide in guides.values() if guide.category == category),
                         key=lambda guide: (guide.title.lower(), guide.id))
        for category in categories
    }
    selected = {
        choices[category][0].id
        for category in required_categories
        if choices[category]
    }

    def screen(window) -> list[str] | None:
        category_index = cursor = 0
        while True:
            category = categories[category_index]
            options = choices[category]
            window.erase()
            height, width = window.getmaxyx()
            requirement = " - selection required" if category in required_categories else ""
            window.addnstr(0, 0, f"{category.title()} ({category_index + 1}/{len(categories)}){requirement}", width - 1)
            window.addnstr(1, 0, "Arrows: move  Space: toggle  Enter: next  Backspace: previous  q: cancel", width - 1)
            for index, guide in enumerate(options):
                marker = "[x]" if guide.id in selected else "[ ]"
                prefix = ">" if index == cursor else " "
                window.addnstr(index + 3, 0, f"{prefix} {marker} {guide.title} - {guide.summary}", width - 1)
            key = window.getch()
            if key in (ord("q"), 27):
                raise ValueError("generation cancelled")
            if key == curses.KEY_UP and options:
                cursor = (cursor - 1) % len(options)
            elif key == curses.KEY_DOWN and options:
                cursor = (cursor + 1) % len(options)
            elif key == ord(" ") and options:
                guide = options[cursor]
                if guide.category in required_categories:
                    selected.difference_update(
                        option.id for option in choices[guide.category]
                    )
                    selected.add(guide.id)
                    continue
                if guide.id in selected:
                    removed = dependents(guides, selected, guide.id)
                    selected.difference_update(removed)
                else:
                    selected.update(item.id for item in resolve_selection(guides, [guide.id]))
            elif key in (curses.KEY_BACKSPACE, 127, 8) and category_index:
                category_index -= 1
                cursor = 0
            elif key in (curses.KEY_ENTER, 10, 13):
                if category_index == len(categories) - 1:
                    return sorted(selected)
                category_index += 1
                cursor = 0

    result = curses.wrapper(screen)
    if result is None:
        raise RuntimeError("interactive selection ended without a result")
    return result


def render(guides: list[Guide], provenance: bool) -> str:
    parts: list[str] = []
    if provenance:
        parts.extend(["---", f"generator-version: {VERSION}",
                      f"source-guides: [{', '.join(guide.id for guide in guides)}]", "---", ""])
    header = next((guide for guide in guides if guide.category == "header"), None)
    parts.extend([f"# {header.title if header else 'Agent Coding Guide'}"])
    if header:
        parts.extend(["", re.sub(r"^# .+\n+", "", header.body, count=1)])
    emitted_sections: set[str] = set()
    for guide in guides:
        if guide.category == "header":
            continue
        if guide.section and guide.section not in emitted_sections:
            section_title = guide.section_title
            if section_title is None:
                raise RuntimeError(f"{guide.path}: validated section is missing a title")
            parts.extend(["", f"## {section_title}"])
            emitted_sections.add(guide.section)
        suppress_title = guide.section in {"structure", "testing"}
        preserve_headings = suppress_title or guide.id == "process"
        body = guide.body if preserve_headings else re.sub(r"^# .+\n+", "", guide.body, count=1)
        heading_offset = 2 if preserve_headings else 1
        body = re.sub(
            r"(?m)^(#{1,%d})(?=\s)" % (6 - heading_offset),
            "#" * heading_offset + r"\1",
            body,
        )
        if suppress_title:
            parts.extend(["", body])
        else:
            parts.extend(["", f"{'###' if guide.section else '##'} {guide.title}", "", body])
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include", action="append", default=[], help="Comma-separated guide IDs; repeatable.")
    parser.add_argument("--output", type=Path, default=Path("AGENTS.md"))
    parser.add_argument("--provenance", action="store_true")
    args = parser.parse_args()
    try:
        root = Path.cwd()
        guides = discover_guides(root, args.output)
        requested = [item.strip() for value in args.include for item in value.split(",") if item.strip()]
        if not requested:
            if not sys.stdin.isatty():
                raise ValueError("use --include when stdin is not interactive")
            requested = choose_interactively(guides)
        selected = resolve_selection(guides, requested)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render(selected, args.provenance), encoding="utf-8")
    except KeyboardInterrupt:
        print("Generation cancelled.", file=sys.stderr)
        return 130
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
