from sqlalchemy import CheckConstraint, DefaultClause, Identity
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex

from db import models  # noqa: F401
from db.base import Base

tables = Base.metadata.tables

total_columns = 0
total_foreign_keys = 0

for table in tables.values():
    total_columns += len(table.columns)
    total_foreign_keys += len(table.foreign_keys)


print(f"Таблиц: {len(tables)}")
print(f"Столбцов: {total_columns}")
print(f"Внешних ключей: {total_foreign_keys}")

for table in tables.values():
    for constraint in table.constraints:
        if isinstance(constraint, CheckConstraint):
            print(f"{table.name} | {constraint.name} | {constraint.sqltext}")

table = tables["categories"]
for index in table.indexes:
    if index.name == "categories_name_normalized_uq":
        print(
            CreateIndex(index).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )

table = tables["payments"]
for index in table.indexes:
    if index.name == "payments_one_active_per_order_idx":
        print(
            CreateIndex(index).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )

table = tables["orders"]
for index in table.indexes:
    if index.name == "orders_user_created_idx":
        print(
            CreateIndex(index).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )

table = tables["payments"]
for index in table.indexes:
    if index.name == "payments_order_created_idx":
        print(
            CreateIndex(index).compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        )

table = tables["users"]

column = table.columns["updated_at"]

print(column.server_default.arg)
print(column.onupdate.arg)

tables = Base.metadata.tables

for table in tables.values():
    for column in table.columns:
        default = column.server_default

        if isinstance(default, DefaultClause):
            print(f"{table.name}.{column.name}: {default.arg}")

        elif isinstance(default, Identity):
            print(f"{table.name}.{column.name}: IDENTITY")
    for column in table.columns:
        if column.onupdate is not None:
            print(f"{table.name}.{column.name}: {column.onupdate.arg}")

    print("\nПроверка внешних ключей и правил ON DELETE:")

for table in tables.values():
    for fk in table.foreign_keys:
        print(
            f"{fk.parent.table.name}.{fk.parent.name} -> "
            f"{fk.column.table.name}.{fk.column.name} | "
            f"ON DELETE {fk.ondelete}"
        )