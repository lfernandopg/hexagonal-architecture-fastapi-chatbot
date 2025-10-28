from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Chat:
    """Entidad Chat - Representa una conversación"""
    
    def __init__(
        self,
        title: str,
        chat_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = chat_id or uuid4()
        self.title = title
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_timestamp(self):
        """Actualiza el timestamp de última modificación"""
        self.updated_at = datetime.utcnow()