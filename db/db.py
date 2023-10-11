import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base


url = URL.create(
    drivername=os.getenv("DRIVER_THEBAZAAR"),
    username=os.getenv("USERNAME_THEBAZAAR"),
    password=os.getenv("PASSWORD_THEBAZAAR"),
    host=os.getenv("HOST_THEBAZAAR"),
    database=os.getenv("DBNAME_THEBAZAAR"),
    port=os.getenv("PORT_THEBAZAAR")
)

engine = create_engine(url)
Base = declarative_base()
make_session = sessionmaker(bind=engine)
session = make_session()
