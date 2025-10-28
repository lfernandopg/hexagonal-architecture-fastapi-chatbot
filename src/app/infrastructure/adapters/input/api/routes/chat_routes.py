from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..schemas.chat_schemas import CreateChatRequest, ChatResponse
from ..schemas.message_schemas import SendMessageRequest, MessageResponse, ChatConversationResponse
from ..dependencies import (
    get_create_chat_use_case,
    get_send_message_use_case,
    get_chat_history_use_case,
    get_list_chats_use_case
)
from ......application.use_cases.create_chat import CreateChatUseCase
from ......application.use_cases.send_message import SendMessageUseCase
from ......application.use_cases.get_chat_history import GetChatHistoryUseCase
from ......application.use_cases.list_chats import ListChatsUseCase
from ......application.dto.chat_dto import CreateChatDTO
from ......application.dto.message_dto import SendMessageDTO
from ......domain.exceptions.domain_exceptions import ChatNotFoundException, DomainException

router = APIRouter(prefix="/api/v1/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    request: CreateChatRequest,
    use_case: CreateChatUseCase = Depends(get_create_chat_use_case)
):
    """Crea un nuevo chat"""
    try:
        dto = CreateChatDTO(title=request.title)
        result = await use_case.execute(dto)
        return result
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ChatResponse])
async def list_chats(
    limit: int = 100,
    offset: int = 0,
    use_case: ListChatsUseCase = Depends(get_list_chats_use_case)
):
    """Lista todos los chats"""
    try:
        result = await use_case.execute(limit=limit, offset=offset)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{chat_id}/messages", response_model=ChatConversationResponse)
async def send_message(
    chat_id: UUID,
    request: SendMessageRequest,
    use_case: SendMessageUseCase = Depends(get_send_message_use_case)
):
    """Envía un mensaje a un chat y obtiene la respuesta del asistente"""
    try:
        dto = SendMessageDTO(chat_id=chat_id, content=request.content)
        user_msg, assistant_msg = await use_case.execute(dto)
        
        return ChatConversationResponse(
            user_message=MessageResponse(**user_msg.__dict__),
            assistant_message=MessageResponse(**assistant_msg.__dict__)
        )
    except ChatNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_history(
    chat_id: UUID,
    use_case: GetChatHistoryUseCase = Depends(get_chat_history_use_case)
):
    """Obtiene el historial completo de mensajes de un chat"""
    try:
        messages = await use_case.execute(chat_id)
        return [MessageResponse(**msg.__dict__) for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
