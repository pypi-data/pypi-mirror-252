import json
import sys

import ftfy

from myclippings.clipping import Clipping

SEPARATOR = "=========="
SECTIONS = {0: "title_and_author", 1: "metadata", 2: "content"}


def clippings_file_to_raw_array(my_clippings_file):
    """Pre-process clippings file into array of clippings"""
    clippings = [{}]

    with open(my_clippings_file, "r", encoding="utf-8") as clippings_file:
        curr_line = 0
        index = 0

        for line in clippings_file:
            # If separator, start new clipping
            if line.strip() == SEPARATOR:
                curr_line = 0
                index += 1
                clippings.append({})
            # Skip empty lines
            elif line.strip() == "":
                continue
            # Clipping lines
            else:
                section = SECTIONS.get(curr_line, "Invalid")
                line = ftfy.fixes.remove_control_chars(line).strip()
                clippings[index][section] = line
                curr_line += 1

    # Remove empty clippings
    filtered_clippings = [clipping for clipping in clippings if clipping]

    return filtered_clippings


def clippings_file_to_parsed_array(my_clippings_file: str):
    books = []
    book_indices = {}  # Dictionary to map book titles to their index in the books list

    raw_clippings_arr = clippings_file_to_raw_array(my_clippings_file)
    parsed_clippings_arr = [
        Clipping(raw_clipping).parsed for raw_clipping in raw_clippings_arr
    ]

    # Group the parsed clippings by book and author
    for clipping in parsed_clippings_arr:
        title = clipping["title"]
        author = clipping["author"]

        if title not in book_indices:
            book_indices[title] = len(books)
            books.append(
                {
                    "title": title,
                    "author": author,
                    "clippings": [],
                }
            )

        book_index = book_indices[title]
        books[book_index]["clippings"].append(
            {
                "note_type": clipping["note_type"],
                "location_start": clipping["location_start"],
                "location_end": clipping["location_end"],
                "date": clipping["date"],
                "content": clipping["content"],
                "content_hash": clipping["content_hash"],
            }
        )

    return books


if __name__ == "__main__":
    file_name = sys.argv[1] if len(sys.argv) > 1 else "My Clippings.txt"
    books = clippings_file_to_parsed_array(file_name)

    # Save as json utf-8 encoded file
    with open("clippings.json", "w", encoding="utf-8") as json_file:
        json.dump(books, json_file, ensure_ascii=False, indent=4)
