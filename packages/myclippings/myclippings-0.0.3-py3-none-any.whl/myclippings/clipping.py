import hashlib
from typing import Any, Dict

from myclippings.parsers import parse_metadata, parse_title_and_author

"""
The constructor takes a raw clipping, validates it, and parses it into a dict (in the parsed setter).
"""


class Clipping:
    def __init__(self, raw_clipping: Dict[str, str]):
        self.raw = raw_clipping
        self.parsed = raw_clipping

    @property
    def raw(self) -> Dict[str, Any]:
        return self._raw

    @raw.setter
    def raw(self, raw_clipping):
        """Validate raw clipping"""
        required_keys = ["title_and_author", "metadata", "content"]
        for key in required_keys:
            if not raw_clipping[key]:
                raise ValueError(
                    f"{key} missing or empty in raw clipping: {raw_clipping}"
                )
        self._raw = raw_clipping

    @property
    def parsed(self) -> Dict[str, Any]:
        return self._parsed

    @parsed.setter
    def parsed(self, raw_clipping) -> Dict[str, Any]:
        """Parse raw clipping into a dict"""
        raw_title_and_author = raw_clipping.get("title_and_author")
        raw_metadata = raw_clipping.get("metadata")
        content = raw_clipping.get("content")

        if not raw_title_and_author or not raw_metadata or not content:
            raise ValueError(f"Invalid raw clipping: {raw_clipping}")

        content_hash = hashlib.sha256(content.encode("utf8")).hexdigest()[:8]
        title, author = parse_title_and_author(raw_title_and_author)
        note_type, location_start, location_end, date = parse_metadata(raw_metadata)

        self._parsed = {
            "content_hash": content_hash,
            "title": title,
            "author": author,
            "note_type": note_type,
            "location_start": location_start,
            "location_end": location_end,
            "date": date,
            "content": content,
        }
