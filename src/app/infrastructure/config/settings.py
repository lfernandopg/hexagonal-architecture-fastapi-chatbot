from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Configuration
    app_name: str = "ChatBot API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "chatbot.db"
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1000
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"