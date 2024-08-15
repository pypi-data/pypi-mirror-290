"""Application for maintaining a personal database of courses and rounds."""

import importlib.metadata
import json

__version__ = importlib.metadata.version(__package__)


def installed_editable() -> bool:
    """Indicate whether golfdb installed in editable (development) mode."""
    dist = importlib.metadata.Distribution.from_name(__package__)
    content = dist.read_text("direct_url.json")
    value = json.loads(content) if content else {}
    return bool(value.get("dir_info", {}).get("editable", False))
