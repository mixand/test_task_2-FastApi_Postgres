import json
import uuid

from typing import Tuple, Any
from pydantic import BaseModel
from sqlalchemy import select

from db import users_db, database, sounds_db


class InputData(BaseModel):
    user_name: str


class UserInfo(BaseModel):
    user_id: int
    user_uuid: str


class InputSound(BaseModel):
    user_id: int
    user_uuid: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class SoundInfo(BaseModel):
    sound_url: str


class UsersDb:
    @staticmethod
    async def post_user_to_db(user_name: str) -> Tuple[int, str]:
        user_uuid: str = str(uuid.uuid1())
        dict_post: dict = {"user": user_name,
                           "user_uuid": user_uuid,
                           }
        query = users_db.insert().values(dict_post)
        user_id = await database.execute(query=query)
        return user_id, user_uuid


class SoundsDb:
    def __init__(self, user_id: int, user_uuid: str, sound_uuid: str):
        self.user_id = user_id
        self.user_uuid = user_uuid
        self.sound_uuid = sound_uuid

    async def post_sound_to_db(self) -> int:
        dict_post: dict = {"sound_uuid": self.sound_uuid,
                           "user_id_check": self.user_id,
                           "user_uuid_check": self.user_uuid,
                           }
        query = sounds_db.insert().values(dict_post)
        sound_id = await database.execute(query=query)
        return sound_id

    async def check_id_and_uuid(self) -> Any:
        query = select(users_db).where(users_db.columns.id == self.user_id,
                                       users_db.columns.user_uuid == self.user_uuid)
        return await database.fetch_one(query)


class GetUuidSound:
    @staticmethod
    async def check_sound_uuid(id_sound: int, id_user: int) -> Any:
        query = select(sounds_db).where(sounds_db.columns.id == id_sound,
                                        sounds_db.columns.user_id_check == id_user)
        result = await database.fetch_one(query)
        if result is not None:
            result = dict(result)["sound_uuid"]
        return result
