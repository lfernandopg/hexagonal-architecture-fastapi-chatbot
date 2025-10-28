from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class SendMessageRequest(BaseModel):
    """Schema para enviar un mensaje"""
    content: str = Field(..., min_length=1, max_length=10000, description="Contenido del mensaje")


class MessageResponse(BaseModel):
    """Schema de respuesta de mensaje"""
    id: UUID
    chat_id: UUID
    role: str
    content: str
    created_at: datetime
    tokens_used: Optional[int] = None
    
    class Config:
        from_attributes = True


class ChatConversationResponse(BaseModel):
    """Schema de respuesta con mensajes del usuario y asistente"""
    user_message: MessageResponse
    assistant_message: MessageResponse