from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CreateChatDTO:
    """DTO para crear un chat"""
    title: str


@dataclass
class ChatDTO:
    """DTO de respuesta para un chat"""
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
