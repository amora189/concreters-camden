from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any


TextHit = tuple[str, Any, str]


def walk_nodes(node: Any, path: str = "$") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(node, list):
        for i, child in enumerate(node):
            yield from walk_nodes(child, f"{path}[{i}]")
        return
    if not isinstance(node, dict):
        return
    yield path, node
    for i, child in enumerate(node.get("elements") or []):
        yield from walk_nodes(child, f"{path}.elements[{i}]")


def widget_text_fields(tree: Any) -> Iterator[TextHit]:
    for path, node in walk_nodes(tree):
        widget_type = node.get("widgetType")
        settings = node.get("settings") or {}
        if widget_type == "heading":
            yield f"{path}.settings.title", settings, "title"
        elif widget_type == "e-heading":
            title = settings.get("title", {}).get("value", {})
            content = title.get("content")
            if isinstance(content, dict):
                yield f"{path}.settings.title.value.content.value", content, "value"
            for i, child in enumerate(title.get("children") or []):
                yield f"{path}.settings.title.value.children[{i}].content", child, "content"
        elif widget_type == "text-editor":
            yield f"{path}.settings.editor", settings, "editor"
        elif widget_type == "e-paragraph":
            paragraph = settings.get("paragraph", {}).get("value", {})
            content = paragraph.get("content")
            if isinstance(content, dict):
                yield f"{path}.settings.paragraph.value.content.value", content, "value"
        elif widget_type == "image-box":
            for key in ("title_text", "description_text"):
                yield f"{path}.settings.{key}", settings, key
            image = settings.get("image")
            if isinstance(image, dict):
                yield f"{path}.settings.image.url", image, "url"
            link = settings.get("link")
            if isinstance(link, dict):
                yield f"{path}.settings.link.url", link, "url"
        elif widget_type == "icon-box":
            for key in ("title_text", "description_text"):
                yield f"{path}.settings.{key}", settings, key
        elif widget_type == "nested-accordion":
            for i, item in enumerate(settings.get("items") or []):
                yield f"{path}.settings.items[{i}].item_title", item, "item_title"
        elif widget_type == "image":
            image = settings.get("image")
            if isinstance(image, dict):
                for key in ("url", "id", "alt"):
                    yield f"{path}.settings.image.{key}", image, key
        elif widget_type == "button":
            yield f"{path}.settings.text", settings, "text"
            link = settings.get("link")
            if isinstance(link, dict):
                yield f"{path}.settings.link.url", link, "url"
        elif widget_type == "google_maps":
            yield f"{path}.settings.address", settings, "address"


def mutate_text(tree: Any, callback: Callable[[str, Any], Any]) -> None:
    for path, holder, key in widget_text_fields(tree):
        if key in holder:
            holder[key] = callback(path, holder[key])

