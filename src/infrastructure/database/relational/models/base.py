from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        dict: JSON,
        list: JSON,
    }
