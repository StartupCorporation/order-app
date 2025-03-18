class DomainModelRepositoryMixin:
    @staticmethod
    def _get_select_columns_string(*args: str) -> str:
        return ", ".join(f'{column} AS "{column}"' for column in args)

    @classmethod
    def _get_inline_placeholders_string(
        cls,
        amount: int,
        start_position: int,
    ) -> str:
        return ", ".join(cls._get_placeholders_tuple(amount=amount, start_position=start_position))

    @staticmethod
    def _get_placeholders_tuple(
        amount: int,
        start_position: int,
    ) -> tuple[str, ...]:
        return tuple(f"${i}" for i in range(start_position, start_position + amount))
