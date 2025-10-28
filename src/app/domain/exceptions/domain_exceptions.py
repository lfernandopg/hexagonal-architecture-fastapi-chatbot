class DomainException(Exception):
    """Excepción base del dominio"""
    pass


class ChatNotFoundException(DomainException):
    """Chat no encontrado"""
    pass


class MessageNotFoundException(DomainException):
    """Mensaje no encontrado"""
    pass


class InvalidChatException(DomainException):
    """Chat inválido"""
    pass