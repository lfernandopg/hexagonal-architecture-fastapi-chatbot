from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from ...domain.value_objects.message_role import MessageRole


@dataclass
class SendMessageDTO:
    """DTO para enviar un mensaje"""
    chat_id: UUID
    content: str


@dataclass
class MessageDTO:
    """DTO de respuesta para un mensaje"""
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    created_at: datetime
    tokens_used: Optional[int] = None