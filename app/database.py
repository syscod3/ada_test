from os import environ, path, getcwd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

# default, if not provided as a env variable
local_db_path = path.abspath(getcwd()) + "/database.db"
DATABASE_PATH = environ.get("DATABASE_PATH", local_db_path)
DATABASE_URL = "sqlite:///{}".format(DATABASE_PATH)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class MessageTable(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, index=True)
    sender = Column(String)
    message = Column(String)
    # cant use datetime because of the Z at the end of the
    created = Column(String)


Base.metadata.create_all(engine)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
