from models.user import UserModel
from db import Base, engine

Base.metadata.create_all(engine)
