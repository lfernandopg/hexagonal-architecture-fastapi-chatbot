import aiosqlite
from typing import Optional


class Database:
    """Gestor de conexión a SQLite"""
    
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self._connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        """Establece conexión con la base de datos"""
        self._connection = await aiosqlite.connect(self.db_path)
        self._connection.row_factory = aiosqlite.Row
        await self._init_db()
    
    async def disconnect(self):
        """Cierra la conexión"""
        if self._connection:
            await self._connection.close()
    
    async def _init_db(self):
        """Inicializa las tablas de la base de datos"""
        async with self._connection.cursor() as cursor:
            # Tabla de chats
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            """)
            
            # Tabla de mensajes
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    chat_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    tokens_used INTEGER,
                    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
                )
            """)
            
            # Índices para mejorar rendimiento
            await cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_chat_id 
                ON messages(chat_id)
            """)
            
            await cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_created_at 
                ON messages(created_at)
            """)
            
            await self._connection.commit()
    
    @property
    def connection(self) -> aiosqlite.Connection:
        """Retorna la conexión activa"""
        if not self._connection:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._connection