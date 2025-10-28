from enum import Enum


class MessageRole(str, Enum):
    """Value Object - Roles posibles de un mensaje"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"