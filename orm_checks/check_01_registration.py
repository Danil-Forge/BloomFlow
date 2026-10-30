import db.models  # noqa: F401
from db.base import Base

tables = Base.metadata.tables

print(f"Количество таблиц: {len(tables)}")
print("\nТаблицы:")

for table_name in tables:
    print(table_name)
