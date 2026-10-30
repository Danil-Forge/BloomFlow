import db.models  # noqa: F401
from db.base import Base

tables = Base.metadata.tables
for table in tables.values():
    print(table.name)
    columns = table.columns

    print(len(columns))

    for column in columns:
        print(
            f"{column.name}: {column.type} | {column.primary_key} | {column.nullable}"
        )

    foreign_keys = table.foreign_keys
    for foreign_key in foreign_keys:
        print(
            f"parent: {foreign_key.parent} | "
            f"column: {foreign_key.column} | "
            f"ondelete: {foreign_key.ondelete}"
        )

    print()
