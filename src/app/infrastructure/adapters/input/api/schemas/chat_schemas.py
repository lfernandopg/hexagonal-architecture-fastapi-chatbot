from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class CreateChatRequest(BaseModel):
    """Schema para crear un chat"""
    title: str = Field(..., min_length=1, max_length=200, description="Título del chat")


class ChatResponse(BaseModel):
    """Schema de respuesta de chat"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True