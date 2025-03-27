import pytest

from domain.service.exception.comment_content_is_long import NoteContentIsLong
from domain.service.value_object.note import Note


def test_note_can_be_created() -> None:
    Note.new(
        content="some content",
    )


def test_note_cant_be_created_with_content_greater_512_chars() -> None:
    with pytest.raises(NoteContentIsLong):
        Note.new(
            content="1" * 513,
        )


def test_note_cant_be_created_with_content_les_1_chars() -> None:
    with pytest.raises(NoteContentIsLong):
        Note.new(
            content="",
        )
