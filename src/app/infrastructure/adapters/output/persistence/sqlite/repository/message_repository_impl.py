from typing import List, Optional
from uuid import UUID
from datetime import datetime

from .....application.ports.output.message_repository import MessageRepository
from .....domain.entities.message import Message
from .....domain.value_objects.message_role import MessageRole
from .connection import Database


class SQLiteMessageRepository(MessageRepository):
    """Implementación SQLite del repositorio de mensajes"""
    
    def __init__(self, database: Database):
        self.db = database
    
    async def save(self, message: Message) -> Message:
        """Guarda un mensaje"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO messages (id, chat_id, role, content, created_at, tokens_used)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(message.id),
                str(message.chat_id),
                message.role.value,
                message.content,
                message.created_at.isoformat(),
                message.tokens_used
            ))
            await self.db.connection.commit()
        
        return message
    
    async def find_by_chat_id(self, chat_id: UUID) -> List[Message]:
        """Obtiene todos los mensajes de un chat ordenados por fecha"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC",
                (str(chat_id),)
            )
            rows = await cursor.fetchall()
            
            return [
                Message(
                    message_id=UUID(row["id"]),
                    chat_id=UUID(row["chat_id"]),
                    role=MessageRole(row["role"]),
                    content=row["content"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    tokens_used=row["tokens_used"]
                )
                for row in rows
            ]
    
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """Busca un mensaje por ID"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM messages WHERE id = ?",
                (str(message_id),)
            )
            row = await cursor.fetchone()
            
            if not row:
                return None
            
            return Message(
                message_id=UUID(row["id"]),
                chat_id=UUID(row["chat_id"]),
                role=MessageRole(row["role"]),
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                tokens_used=row["tokens_used"]
            )