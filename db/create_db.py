from db.db import Base, engine
from models.user import UserModel

# I should use alembic to manage migrations but for now this file should handle DDL operations (shame on me)
Base.metadata.create_all(engine)
