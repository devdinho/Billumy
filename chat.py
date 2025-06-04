from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
from bson import ObjectId
import uuid

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatData(BaseModel):
    model: str = "billumy"
    messages: List[Message]
    stream: bool = True

class ChatCreate(BaseModel):
    user_id: str
    data: ChatData

class ChatUpdate(BaseModel):
    title: Optional[str] = None
    data: ChatData

class ChatInDB(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex, alias="id")
    user_id: str
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    data: ChatData

    class Config:
        validate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }