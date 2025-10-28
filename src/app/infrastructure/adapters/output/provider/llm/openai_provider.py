from typing import List, Dict
import openai
from openai import AsyncOpenAI

from ....application.ports.output.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """Implementación del proveedor OpenAI"""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ) -> Dict[str, any]:
        """
        Genera una respuesta usando la API de OpenAI
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            model: Modelo a utilizar
            temperature: Creatividad de la respuesta (0-2)
        
        Returns:
            Dict con 'content' y 'tokens_used'
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": model
            }
        
        except openai.APIError as e:
            raise Exception(f"Error de API de OpenAI: {str(e)}")
        except openai.RateLimitError as e:
            raise Exception(f"Límite de tasa excedido: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al generar respuesta: {str(e)}")