from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, TypedDict

from pydantic import BaseModel


class ToolDefinition(TypedDict):
    title: str
    type: str
    description: str
    properties: dict[str, object]
    required: list[str]


class Tool(BaseModel, ABC):
    @classmethod
    @lru_cache
    def definition(cls) -> ToolDefinition:
        _schema = cls.model_json_schema()
        return {
            "title": cls.__name__,
            "type": "object",
            "description": cls.__doc__ or "[No description]",
            "properties": _schema.get("properties", {}),
            "required": _schema.get("required", []),
        }

    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError
