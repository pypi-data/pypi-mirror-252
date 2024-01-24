import re

import dateparser

DEFAULT_DATE = "1970-01-01T00:00:00"
TRANSLATIONS = {
    "note_type": {
        "note": ["note", "nota"],
        "highlight": ["highlight", "subrayado"],
        "bookmark": ["bookmark", "marcador"],
    },
    "location": ["Location", "posición"],
}

title_author_regex = re.compile(
    r"(?P<title>.+)(?:\(|\[|\-)(?P<author>(?<=\(|\[|\-).+?(?=\)|\]|$))"
)
position_regex = re.compile(r"(\d+)-?(\d+)?")


def parse_title_and_author(title_and_author: str):
    """Parse title and author from the raw clipping."""
    result = title_author_regex.findall(title_and_author)
    if result:
        title, author = result[0]
        title = title.strip()
        author = author.strip()
        return title, author
    else:
        for word in TRANSLATIONS["location"]:
            if word in title_and_author.lower():
                return "", ""

        return title_and_author, ""


def parse_metadata(metadata: str) -> tuple:
    """Parse metadata from the raw clipping."""
    result = metadata.split("|")
    is_complete = len(result) == 3

    note_type = parse_note_type(result[0])
    location = parse_location(result[1]) if is_complete else {}
    location_start = location.get("start")
    location_end = location.get("end")
    date = parse_date(result[2]) if is_complete else DEFAULT_DATE

    return note_type, location_start, location_end, date


def parse_location(raw_location: str) -> dict:
    """Parse location into a tuple."""
    try:
        result = position_regex.findall(raw_location)
        if result:
            start, end = result[0]
            start = int(start) if start else None
            end = int(end) if end else None
            return {
                "start": start,
                "end": end,
            }
    except Exception:
        print(f"Error parsing location: {raw_location}")
        return {}


def parse_date(raw_date: str):
    """Parse date into a tuple."""
    try:
        result = raw_date.replace(",", "").split(" ")

        # Keep only needed words to avoid multilingual issues
        result = [
            word
            for word in result
            if len(word) > 2 or word.isdigit() or word in ["AM", "PM"]
        ]

        is_12hr_format = result[-1] in ["AM", "PM"]
        month = result[2]
        day = result[3]
        year = result[4]
        time = result[5] + " " + result[6] if is_12hr_format else result[5]

        date = day + " " + month + " " + year + " " + time
        date = dateparser.parse(date).isoformat()

        return date

    except Exception as e:
        print(f"Error parsing date: {raw_date}")
        print(e)
        return None


def parse_note_type(raw_note_type: str):
    """Parse note type into a string."""
    try:
        for key, value in TRANSLATIONS["note_type"].items():
            if any(word in raw_note_type.lower() for word in value):
                return key
    except Exception:
        print(f"Error parsing note type: {raw_note_type}")
        return None
