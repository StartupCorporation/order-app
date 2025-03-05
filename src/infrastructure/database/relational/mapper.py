from infrastructure.database.relational.models.base import Base
from infrastructure.database.relational.models.comment import Comment as CommentTable
from domain.comment.entity import Comment


class DatabaseToEntityMapper:

    def __init__(self):
        self._mapping_configuration = {
            Comment: {
                "table": CommentTable.__table__,
            },
        }

    def map(self) -> None:
        mapper_registry = Base.registry

        for entity, mapping_config in self._mapping_configuration.items():
            mapper_registry.map_imperatively(
                class_=entity,
                local_table=mapping_config["table"],
                properties=mapping_config.get("properties"),
            )
