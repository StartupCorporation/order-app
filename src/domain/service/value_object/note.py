from dataclasses import dataclass

from dw_shared_kernel import StringLengthSpecification, ValueObject

from domain.service.exception.comment_content_is_long import NoteContentIsLong


@dataclass(kw_only=True, slots=True)
class Note(ValueObject):
    content: str

    @classmethod
    def new(
        cls,
        content: str,
    ) -> "Note":
        cls._check_content(content=content)

        return Note(
            content=content,
        )

    @staticmethod
    def _check_content(content: str) -> None:
        if not StringLengthSpecification(min_length=1, max_length=512).is_satisfied_by(value=content):
            raise NoteContentIsLong()
