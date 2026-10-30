import asyncio

from sqlalchemy import text

from db.session import SessionFactory, engine


async def main() -> None:
    try:
        async with SessionFactory() as session:
            result = await session.execute(
                text("SELECT current_database(), current_user")
            )
            database_name, role_name = result.one()

            number = await session.scalar(text("SELECT 1"))

            print(f"База: {database_name}")
            print(f"Пользователь: {role_name}")
            print(f"Результат SELECT 1: {number}")
            print("Подключение к PostgreSQL успешно")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
