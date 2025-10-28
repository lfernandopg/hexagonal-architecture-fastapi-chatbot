from typing import List
from ..dto.chat_dto import ChatDTO
from ..ports.output.chat_repository import ChatRepository


class ListChatsUseCase:
    """Caso de uso: Listar todos los chats"""
    
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository
    
    async def execute(self, limit: int = 100, offset: int = 0) -> List[ChatDTO]:
        """Lista todos los chats"""
        chats = await self.chat_repository.find_all(limit, offset)
        
        return [
            ChatDTO(
                id=chat.id,
                title=chat.title,
                created_at=chat.created_at,
                updated_at=chat.updated_at
            )
            for chat in chats
        ]