import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# on unix enviroments these variables should be exported on .bashrc ou .zshrc files
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

# every interaction with database has it own session to perform actions
# note: think about how to scale the database when going to production
session = make_session()
