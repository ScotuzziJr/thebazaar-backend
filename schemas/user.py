from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class UserSerializer(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    email: str | None = None
    password: str
    
    class Config:
        orm_mode=True