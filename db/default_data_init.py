import asyncio
import os
import uuid
import psycopg2

from dotenv import load_dotenv
from sqlalchemy import select

from db.database import async_session_factory
from db.models import AppUsers, Roles, Permissions, Employers, TelegramUsers, RolePermissions
from langchain_openai import OpenAIEmbeddings
from psycopg2.extras import execute_values

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
embeddings_model = OpenAIEmbeddings()


async def init_role(session_factory):
    async with session_factory() as session:
        try:
            role_admin = Roles(id=uuid.uuid4(), name='Admin', description='Head admin')
            role_user = Roles(id=uuid.uuid4(), name='User', description='user')
            role_guest = Roles(id=uuid.uuid4(), name='Guest', description='guest')
            role_librarian = Roles(id=uuid.uuid4(), name='Librarian', description='librarian')
            session.add_all([role_admin, role_user, role_guest, role_librarian])
            await session.commit()
            return role_admin.id
        except Exception as e:
            await session.rollback()
            raise e


async def init_permissions(session_factory):
    permissions_data = []
    categories = ["book", "location", "order", "wishlist"]
    operations = [
        "create",
        "update_all", "update_own",
        "read_all", "read_own",
        "delete_all", "delete_own"
    ]

    for category in categories:
        for operation in operations:
            permissions_data.append({
                "name": f"{operation}_{category}",
                "description": f"{operation.replace('_', ' ').capitalize()} permission for {category}"
            })

    async with session_factory() as session:
        try:
            for perm in permissions_data:
                existing = await session.execute(
                    select(Permissions).where(Permissions.name == perm["name"])
                )
                if not existing.scalar_one_or_none():
                    permission = Permissions(
                        id=uuid.uuid4(),
                        name=perm["name"],
                        description=perm["description"]
                    )
                    session.add(permission)

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e


async def init_role_permissions(session_factory):
    async with session_factory() as session:
        try:
            roles_result = await session.execute(select(Roles))
            roles = {role.name: role.id for role in roles_result.scalars().all()}

            perms_result = await session.execute(select(Permissions))
            permissions = {perm.name: perm.id for perm in perms_result.scalars().all()}

            role_permissions = []

            for perm_id in permissions.values():
                role_permissions.append(
                    RolePermissions(role_id=roles["Admin"], permission_id=perm_id)
                )

            librarian_perms = [
                "read_all_location", "update_location",
                "read_all_wishlist",
                "read_all_book", "update_book", "delete_book", "create_book",
                "update_own_order", "read_own_order", "create_order"
            ]
            for perm_name in librarian_perms:
                if perm_name in permissions:
                    role_permissions.append(
                        RolePermissions(role_id=roles["Librarian"], permission_id=permissions[perm_name])
                    )

            user_perms = [
                "read_location",
                "update_own_user",
                "read_book", "create_book",
                "update_own_order", "read_own_order", "create_order",
                "update_own_wishlist", "delete_own_wishlist", "create_wishlist"
            ]
            for perm_name in user_perms:
                if perm_name in permissions:
                    role_permissions.append(
                        RolePermissions(role_id=roles["User"], permission_id=permissions[perm_name])
                    )

            guest_perms = [
                "read_location",
                "read_book",
                "read_own_order",
                "create_order"
            ]
            for perm_name in guest_perms:
                if perm_name in permissions:
                    role_permissions.append(
                        RolePermissions(role_id=roles["Guest"], permission_id=permissions[perm_name])
                    )

            for rp in role_permissions:
                exists = await session.execute(
                    select(RolePermissions).where(
                        RolePermissions.role_id == rp.role_id,
                        RolePermissions.permission_id == rp.permission_id
                    )
                )
                if not exists.scalar_one_or_none():
                    session.add(rp)

            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e


async def init_employer(session_factory) -> uuid.UUID:
    full_name = os.getenv('ADMIN_FULL_NAME')
    email = os.getenv('ADMIN_EMAIL')

    async with session_factory() as session:
        employer = Employers(
            id=uuid.uuid4(),
            full_name=full_name,
            email=email,
            is_verified=True,
        )
        session.add(employer)
        await session.commit()
        return employer.id


async def init_telegram_user(session_factory) -> uuid.UUID:
    tg_str = os.getenv("ADMIN_TG_ID")

    async with session_factory() as session:
        new_tg_user = TelegramUsers(
            id=uuid.uuid4(),
            telegram_id=tg_str,
            username=os.getenv("ADMIN_FULL_NAME"),
        )
        session.add(new_tg_user)
        await session.commit()
        return new_tg_user.id


async def admin_init(session_factory):
    telegram_user_id = await init_telegram_user(session_factory)
    employer_id = await init_employer(session_factory)
    role_id = await init_role(session_factory)
    async with session_factory() as session:
        admin = AppUsers(
            telegram_user_id=telegram_user_id,
            employer_id=employer_id,
            role_id=role_id,
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        return True


async def init_books():
    default_books = [
        {"title": "Python Basics", "description": "Learn Python step by step", "author": "John Smith"},
        {"title": "Advanced Python", "description": "Deep dive into Python", "author": "Alice Brown"},
        {"title": "AI for Beginners", "description": "Introduction to AI", "author": "David Lee"},
        {"title": "Machine Learning 101", "description": "ML fundamentals", "author": "Emma Davis"},
        {"title": "Data Science Handbook", "description": "Essential DS skills", "author": "Michael Johnson"},
        {"title": "Web Development with FastAPI", "description": "Build APIs with FastAPI", "author": "Olivia Wilson"},
        {"title": "SQL for Data Analysis", "description": "SQL queries for beginners", "author": "Chris Martin"},
        {"title": "Clean Code", "description": "Writing maintainable code", "author": "Robert C. Martin"},
        {"title": "Algorithms Unlocked", "description": "Intro to algorithms", "author": "Thomas Cormen"},
        {"title": "Deep Learning Simplified", "description": "Deep learning basics", "author": "Sarah Walker"},
    ]

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    records = []
    for book in default_books:
        text = f"{book['title']} {book['description']} {book['author']}"
        vector = embeddings_model.embed_query(text)
        vector = [float(v) for v in vector]

        records.append((
            str(uuid.uuid4()), book["title"], book["description"], book["author"], vector
        ))

    insert_query = """
        INSERT INTO books (id, title, description, author, embedding)
        VALUES %s
    """

    with conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_query, records)


async def main(session_factory):
    await init_books()
    await admin_init(session_factory)
    await init_permissions(session_factory)
    await init_role_permissions(session_factory)


if __name__ == '__main__':
    asyncio.run(main(async_session_factory))
