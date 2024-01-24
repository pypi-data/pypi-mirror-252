import pytest

from myclippings.parsers import (
    parse_date,
    parse_metadata,
    parse_note_type,
    parse_title_and_author,
)
from tests.test_cases import (
    date_tests,
    metadata_tests,
    note_type_tests,
    title_and_author_tests,
)


@pytest.mark.parametrize("testcase", title_and_author_tests)
def test_parse_title_and_author(testcase):
    input_data, expected_title, expected_author = testcase

    title, author = parse_title_and_author(input_data)

    assert title == expected_title
    assert author == expected_author


@pytest.mark.parametrize("testcase", metadata_tests)
def test_metadata(testcase):
    (
        input_data,
        expected_note_type,
        expected_location_start,
        expected_location_end,
        expected_date,
    ) = testcase

    note_type, location_start, location_end, date = parse_metadata(input_data)

    assert note_type == expected_note_type
    assert location_start == expected_location_start
    assert location_end == expected_location_end
    assert date == expected_date


@pytest.mark.parametrize("testcase", date_tests)
def test_date(testcase):
    input_data, expected_date = testcase

    date = parse_date(input_data)

    assert date == expected_date


@pytest.mark.parametrize("testcase", note_type_tests)
def test_note_type(testcase):
    input_data, expected_note_type = testcase

    note_type = parse_note_type(input_data)

    assert note_type == expected_note_type
