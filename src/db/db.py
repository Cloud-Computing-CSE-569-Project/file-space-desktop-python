import sqlalchemy
import databases
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./my_db.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

files = sqlalchemy.Table(
    "files",
    metadata,
    Column("id", Integer, primary_key = True, autoincrement= True),
    Column("object_id", String(512), nullable = False),
    Column("is_folder", Boolean, nullable = False),
    Column("last_modified", DateTime, nullable = False),
    Column("file_path", String(255), nullable = False),
    Column("file_name", String(255), nullable=False),
    Column("version", String(255)),
    UniqueConstraint("object_id"),
    UniqueConstraint("file_name")
)

logins = sqlalchemy.Table(
    "logins",
    metadata,
    Column("id", Integer, primary_key = True, autoincrement = True),
    Column("username", String(255), nullable= False),
    Column("isLogged",Boolean, default = "True"),
    Column("refreshToken", String(255)),
    Column("accessToken", String(255))

)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args = {"check_same_thread": False})

metadata.create_all(engine)
session = sessionmaker(bind=engine)