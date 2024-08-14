from typing import Any
from pydantic import BaseModel, Field
from .base import _ScikitCompact, TaskModel

TASK_NAME = "ollama"
QUEUE_NAME = "ollama-h4cv"


class OllamaModel(TaskModel):
    """ollama"""

    name: str = TASK_NAME
    queue_name: str = QUEUE_NAME


class OllamaData(BaseModel):
    prompt: str = Field(max_length=4096)
    image_urls: list = Field(default=[], description="list of image urls")
    max_tokens: int = 1024
    model_name: str = "openbmb/MiniCPM-Llama3-V-2_5"


class OllamaTask(_ScikitCompact):
    """Ollama task"""

    def handle(self, data: OllamaData) -> Any:
        pass
