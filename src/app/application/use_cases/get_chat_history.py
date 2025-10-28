from uuid import UUID
from typing import List
from ..dto.message_dto import MessageDTO
from ..ports.output.message_repository import MessageRepository


class GetChatHistoryUseCase:
    """Caso de uso: Obtener historial de un chat"""
    
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository
    
    async def execute(self, chat_id: UUID) -> List[MessageDTO]:
        """Obtiene todos los mensajes de un chat"""
        messages = await self.message_repository.find_by_chat_id(chat_id)
        
        return [
            MessageDTO(
                id=msg.id,
                chat_id=msg.chat_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
                tokens_used=msg.tokens_used
            )
            for msg in messages
        ]