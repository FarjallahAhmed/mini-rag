from enum import Enum

class LLMEnum(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnum(Enum):
    SYSTEM="system"
    ASSISTANT="assistant"
    USER="user"