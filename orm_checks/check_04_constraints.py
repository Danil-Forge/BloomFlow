from db import models  # noqa: F401
from db.base import Base

tables = Base.metadata.tables

for table in tables.values():
    print(f"\nИмя таблицы: {table.name}")

    print("Ограничения:")
    for constraint in table.constraints:
        print(
            f"{constraint.name} | "
            f"{type(constraint).__name__}"
        )

    print("Индексы:")
    for index in table.indexes:
        print(f"Индекс: {index.name} | unique={index.unique}")

        for column in index.columns:
            print(f"Столбец: {column.name}")

    print()
   

