from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...domain.entities.chat import Chat


class ChatRepository(ABC):
    """Puerto de salida - Repositorio de Chats"""
    
    @abstractmethod
    async def save(self, chat: Chat) -> Chat:
        """Guarda un chat"""
        pass
    
    @abstractmethod
    async def find_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """Busca un chat por ID"""
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Chat]:
        """Lista todos los chats"""
        pass
    
    @abstractmethod
    async def delete(self, chat_id: UUID) -> bool:
        """Elimina un chat"""
        pass