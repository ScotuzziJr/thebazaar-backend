from sqlalchemy import String, Column
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base

class UserModel(Base):
    __tablename__ = "thebazaar_users"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User id={self.user_id}, username={self.username}, email={self.email}, password={self.password}>"
