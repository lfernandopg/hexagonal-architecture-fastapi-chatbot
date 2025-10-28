from uuid import UUID
from ..dto.chat_dto import CreateChatDTO, ChatDTO
from ..ports.output.chat_repository import ChatRepository
from ...domain.entities.chat import Chat


class CreateChatUseCase:
    """Caso de uso: Crear un nuevo chat"""
    
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository
    
    async def execute(self, dto: CreateChatDTO) -> ChatDTO:
        """Crea un nuevo chat"""
        chat = Chat(title=dto.title)
        saved_chat = await self.chat_repository.save(chat)
        
        return ChatDTO(
            id=saved_chat.id,
            title=saved_chat.title,
            created_at=saved_chat.created_at,
            updated_at=saved_chat.updated_at
        )
