import os
from openai import OpenAI
from typing import List, Dict, Tuple

client = OpenAI()

def get_chat_response(model_name: str, messages: List[Dict[str, str]]) -> Tuple[str, int, int]:
    """
    відправляє запит до OpenAI та повертає:
    (текст_відповіді, prompt_tokens, completion_tokens)
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    
    content = response.choices[0].message.content
    usage = response.usage
    
    return content, usage.prompt_tokens, usage.completion_tokens
