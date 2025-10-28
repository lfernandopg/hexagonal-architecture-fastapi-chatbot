from functools import lru_cache
from typing import Generator

from ....config.settings import Settings
from .....application.use_cases.create_chat import CreateChatUseCase
from .....application.use_cases.send_message import SendMessageUseCase
from .....application.use_cases.get_chat_history import GetChatHistoryUseCase
from .....application.use_cases.list_chats import ListChatsUseCase
from ...output.persistence.sqlite.connection import Database
from ...output.persistence.sqlite.chat_repository_impl import SQLiteChatRepository
from ...output.persistence.sqlite.message_repository_impl import SQLiteMessageRepository
from ...output.external.openai_provider import OpenAIProvider


@lru_cache()
def get_settings() -> Settings:
    """Obtiene configuración de la aplicación"""
    return Settings()


# Instancias globales (se inicializan en el startup de FastAPI)
_database: Database = None
_chat_repository: SQLiteChatRepository = None
_message_repository: SQLiteMessageRepository = None
_llm_provider: OpenAIProvider = None


async def init_dependencies():
    """Inicializa las dependencias globales"""
    global _database, _chat_repository, _message_repository, _llm_provider
    
    settings = get_settings()
    
    _database = Database(settings.database_url)
    await _database.connect()
    
    _chat_repository = SQLiteChatRepository(_database)
    _message_repository = SQLiteMessageRepository(_database)
    _llm_provider = OpenAIProvider(settings.openai_api_key)


async def close_dependencies():
    """Cierra las dependencias globales"""
    global _database
    if _database:
        await _database.disconnect()


def get_create_chat_use_case() -> CreateChatUseCase:
    """Inyección de dependencia para CreateChatUseCase"""
    return CreateChatUseCase(_chat_repository)


def get_send_message_use_case() -> SendMessageUseCase:
    """Inyección de dependencia para SendMessageUseCase"""
    return SendMessageUseCase(_chat_repository, _message_repository, _llm_provider)


def get_chat_history_use_case() -> GetChatHistoryUseCase:
    """Inyección de dependencia para GetChatHistoryUseCase"""
    return GetChatHistoryUseCase(_message_repository)


def get_list_chats_use_case() -> ListChatsUseCase:
    """Inyección de dependencia para ListChatsUseCase"""
    return ListChatsUseCase(_chat_repository)