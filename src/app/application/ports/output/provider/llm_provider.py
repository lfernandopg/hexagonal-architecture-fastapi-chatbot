from abc import ABC, abstractmethod
from typing import List, Dict


class LLMProvider(ABC):
    """Puerto de salida - Proveedor de LLM (Large Language Model)"""
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ) -> Dict[str, any]:
        """Genera una respuesta del LLM"""
        pass