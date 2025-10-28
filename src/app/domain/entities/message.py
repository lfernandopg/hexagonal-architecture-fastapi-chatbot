from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from ..value_objects.message_role import MessageRole


class Message:
    """Entidad Message - Representa un mensaje en un chat"""
    
    def __init__(
        self,
        chat_id: UUID,
        role: MessageRole,
        content: str,
        message_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        tokens_used: Optional[int] = None
    ):
        self.id = message_id or uuid4()
        self.chat_id = chat_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.utcnow()
        self.tokens_used = tokens_used
        
        self._validate()
    
    def _validate(self):
        """Valida las reglas de negocio del mensaje"""
        if not self.content.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío")
        
        if len(self.content) > 10000:
            raise ValueError("El mensaje excede el límite de caracteres permitidos")
