# myclippings

---

Converts `My Clippings.txt` file into a JSON format like below:

```json
[
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Martin, Robert C.",
  "clippings": [
    {
        "content_hash": "66698d9e",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Martin, Robert C.",
        "note_type": "highlight",
        "location_start": 892,
        "location_end": 893,
        "date": "2022-10-12T12:20:59",
        "content": "Leave the campground cleaner than you found it.5"
    },
    {
        "content_hash": "f31e9873",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Martin, Robert C.",
        "note_type": "highlight",
        "location_start": 783,
        "location_end": 783,
        "date": "2022-10-03T14:55:50",
        "content": "Code, without tests, is not clean. No matter how elegant it is,"
    }
  ]
]
```

Currently, it supports English and Spanish languages.

## Usage

As a CLI tool:

```bash
python3 -m myclippings.main "My Clippings.txt"
```

As a module:

```bash
pip install myclippings
```

```python
from myclippings import clippings_to_json

books = clippings_to_json("My Clippings.txt")
```
