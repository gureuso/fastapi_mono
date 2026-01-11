from common.database.mysql.write import write_database, user_table
from common.database.mysql.entity import UserEntity
from pydantic import EmailStr

from common.random import fixed_length_from_key


class UserService:
    @staticmethod
    async def create(user_entity: UserEntity) -> UserEntity:
        query = user_table.insert().values(email=user_entity.email, provider=user_entity.provider, created_at=user_entity.created_at)
        ai = await write_database.execute(query)
        user_entity.id = ai
        user_entity.num = fixed_length_from_key(str(ai), 10)
        return user_entity

    @staticmethod
    async def find_one_by_id(user_id: int):
        query = user_table.select().where(user_table.c.id == user_id)
        row = await write_database.fetch_one(query)
        return UserEntity(**dict(row)) if row else None

    @staticmethod
    async def find_one_by_email(email: EmailStr):
        query = user_table.select().where(user_table.c.email == email)
        row = await write_database.fetch_one(query)
        return UserEntity(**dict(row)) if row else None

    @staticmethod
    async def delete_by_id(user_id: int):
        query = """
            DELETE FROM User WHERE id = :user_id
        """
        await write_database.execute(query, {'user_id': user_id})
        return {}

    @staticmethod
    async def update_num(user: UserEntity):
        query = """
            UPDATE User SET num = :num WHERE id = :user_id;
        """
        await write_database.execute(query, {'num': user.num, 'user_id': user.id})
        return {}
