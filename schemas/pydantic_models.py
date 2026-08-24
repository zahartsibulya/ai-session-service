from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Текст повідомлення користувача")   #Field перевіряє, щоб повідомлення не було порожнім

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    tokens_used: int
    cost: float
    created_at: datetime

    class Config:
        from_attributes = True  #дозволяє читати дані прямо з об'єктів SQLAlchemy

class SessionCreate(BaseModel):
    model_name: Optional[str] = "gpt-4o-mini"

class SessionResponse(BaseModel):
    id: str
    model_name: str
    total_tokens: int
    total_cost: float
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
