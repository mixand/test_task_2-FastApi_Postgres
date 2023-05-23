from databases import Database
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, ForeignKey

from data_env import user_value, password_value, host_value, port_value, database_value

SQLALCHEMY_DATABASE_URL = f'postgresql://{user_value}:{password_value}@{host_value}:{port_value}/{database_value}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

users_db = Table(
    "users_db",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user", String),
    Column("user_uuid", String, unique=True),
)

sounds_db = Table(
    "sounds_db",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sound_uuid", String, unique=True),
    Column("user_id_check", Integer, ForeignKey("users_db.id")),
    Column("user_uuid_check", String, ForeignKey("users_db.user_uuid")),
)

database = Database(SQLALCHEMY_DATABASE_URL)
