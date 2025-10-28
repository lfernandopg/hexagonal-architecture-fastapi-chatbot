from ..dto.message_dto import SendMessageDTO, MessageDTO
from ..ports.output.chat_repository import ChatRepository
from ..ports.output.message_repository import MessageRepository
from ..ports.output.llm_provider import LLMProvider
from ...domain.entities.message import Message
from ...domain.value_objects.message_role import MessageRole
from ...domain.exceptions.domain_exceptions import ChatNotFoundException


class SendMessageUseCase:
    """Caso de uso: Enviar un mensaje y obtener respuesta del LLM"""
    
    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: MessageRepository,
        llm_provider: LLMProvider
    ):
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.llm_provider = llm_provider
    
    async def execute(self, dto: SendMessageDTO) -> tuple[MessageDTO, MessageDTO]:
        """
        Envía un mensaje del usuario y obtiene respuesta del asistente
        Retorna: (mensaje_usuario, mensaje_asistente)
        """
        # Verificar que el chat existe
        chat = await self.chat_repository.find_by_id(dto.chat_id)
        if not chat:
            raise ChatNotFoundException(f"Chat {dto.chat_id} no encontrado")
        
        # Crear y guardar mensaje del usuario
        user_message = Message(
            chat_id=dto.chat_id,
            role=MessageRole.USER,
            content=dto.content
        )
        saved_user_message = await self.message_repository.save(user_message)
        
        # Obtener historial de mensajes
        history = await self.message_repository.find_by_chat_id(dto.chat_id)
        messages_for_llm = [
            {"role": msg.role.value, "content": msg.content}
            for msg in history
        ]
        
        # Obtener respuesta del LLM
        llm_response = await self.llm_provider.generate_response(messages_for_llm)
        
        # Crear y guardar mensaje del asistente
        assistant_message = Message(
            chat_id=dto.chat_id,
            role=MessageRole.ASSISTANT,
            content=llm_response["content"],
            tokens_used=llm_response.get("tokens_used")
        )
        saved_assistant_message = await self.message_repository.save(assistant_message)
        
        # Actualizar timestamp del chat
        chat.update_timestamp()
        await self.chat_repository.save(chat)
        
        return (
            self._to_dto(saved_user_message),
            self._to_dto(saved_assistant_message)
        )
    
    def _to_dto(self, message: Message) -> MessageDTO:
        """Convierte Message a MessageDTO"""
        return MessageDTO(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            tokens_used=message.tokens_used
        )