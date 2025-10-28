from typing import List, Optional
from uuid import UUID
from datetime import datetime
import aiosqlite

from .....application.ports.output.chat_repository import ChatRepository
from .....domain.entities.chat import Chat
from .connection import Database


class SQLiteChatRepository(ChatRepository):
    """Implementación SQLite del repositorio de chats"""
    
    def __init__(self, database: Database):
        self.db = database
    
    async def save(self, chat: Chat) -> Chat:
        """Guarda o actualiza un chat"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute("""
                INSERT OR REPLACE INTO chats (id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (
                str(chat.id),
                chat.title,
                chat.created_at.isoformat(),
                chat.updated_at.isoformat()
            ))
            await self.db.connection.commit()
        
        return chat
    
    async def find_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """Busca un chat por ID"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM chats WHERE id = ?",
                (str(chat_id),)
            )
            row = await cursor.fetchone()
            
            if not row:
                return None
            
            return Chat(
                chat_id=UUID(row["id"]),
                title=row["title"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"])
            )
    
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Chat]:
        """Lista todos los chats"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM chats ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = await cursor.fetchall()
            
            return [
                Chat(
                    chat_id=UUID(row["id"]),
                    title=row["title"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"])
                )
                for row in rows
            ]
    
    async def delete(self, chat_id: UUID) -> bool:
        """Elimina un chat"""
        async with self.db.connection.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM chats WHERE id = ?",
                (str(chat_id),)
            )
            await self.db.connection.commit()
            return cursor.rowcount > 0