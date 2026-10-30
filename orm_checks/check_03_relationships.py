from sqlalchemy.orm import configure_mappers

from db import models  # noqa: F401
from db.base import Base

configure_mappers()

print("ORM-модели успешно настроены")

mappers = Base.registry.mappers

for mapper in mappers:
    print(mapper.class_.__name__)

    relationships = mapper.relationships

    for relationship in relationships:
        print(
            f"key: {relationship.key} | "
            f"uselist: {relationship.uselist} | "
            f"direction: {relationship.direction} | "
            f"back_populates: {relationship.back_populates} | "
        )
    print()
