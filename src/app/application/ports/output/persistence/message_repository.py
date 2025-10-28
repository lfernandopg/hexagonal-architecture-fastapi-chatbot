from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...domain.entities.message import Message


class MessageRepository(ABC):
    """Puerto de salida - Repositorio de Mensajes"""
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        """Guarda un mensaje"""
        pass
    
    @abstractmethod
    async def find_by_chat_id(self, chat_id: UUID) -> List[Message]:
        """Obtiene todos los mensajes de un chat"""
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """Busca un mensaje por ID"""
        pass
