import sys
import os

# Разрешение имотра
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db import get_db
from db.models import Author, Publisher, Reader, Book, Issuance  # noqa


from faker import Faker
from random import choice
from typing import Collection
from tqdm import tqdm
from random import randint, uniform
import asyncio

# Генератор фейковых данных
fake = Faker("ru_RU")

# Количество фикстур
NUM_AUTHORS = 10
NUM_PUBLISHERS = 5
NUM_BOOKS = 20
NUM_READERS = 15
NUM_ISSUES = 30


async def create_objects(obj_collection: Collection):
    async for session in get_db():
        session.add_all(obj_collection)
        await session.commit()

        for obj in obj_collection:
            await session.refresh(obj)


async def main():
    print("\nГенерация Authors:")
    authors = [Author(name=fake.name()) for _ in tqdm(range(NUM_AUTHORS))]
    await create_objects(authors)

    print("\nГенерация Publishers:")
    publishers = [
        Publisher(
            name=fake.company(),
            city=fake.city(),
        )
        for _ in tqdm(range(NUM_PUBLISHERS))
    ]
    await create_objects(publishers)

    print("\nГенерация Readers:")
    readers = [
        Reader(
            full_name=fake.name(),
            phone=fake.numerify("+7(9##)###-##-##"),
            address=fake.address(),
        )
        for _ in tqdm(range(NUM_READERS))
    ]
    await create_objects(readers)

    print("\nГенерация Books:")
    books = [
        Book(
            title=fake.sentence(nb_words=3),
            author_code=choice(authors).code,
            publisher_code=choice(publishers).code,
            publishing_year=randint(1500, 2070),
            price=round(uniform(10, 10000), 2),
            amount=randint(5, 100),
        )
        for _ in tqdm(range(NUM_BOOKS))
    ]
    await create_objects(books)

    print("\nГенерация Issuances:")
    issuances = [
        Issuance(
            book_code=choice(books).code,
            reader_code=choice(readers).code,
            issuanced_at=fake.date_between(start_date="-1y", end_date="today"),
            expires_at=fake.date_between(start_date="today", end_date="+20d"),
        )
        for _ in tqdm(range(NUM_ISSUES))
    ]
    await create_objects(issuances)


if __name__ == "__main__":
    asyncio.run(main())
