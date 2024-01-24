import json
from functools import cached_property
from typing import AsyncIterator, Literal, Type

from jinja2 import Template
from ollama import AsyncClient  # type: ignore
from pydantic import BaseModel, Field

from .proxy import LazyProxy
from .tool import Tool


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class Agent(BaseModel, LazyProxy[AsyncClient]):
    messages: list[Message] = []
    model: str = Field(default="mistral:instruct")
    tools: list[Type[Tool]] = Field(default_factory=Tool.__subclasses__)

    @cached_property
    def template(self):
        return Template(
            """
		[INST]
		Based on user input determine if a tool call is gonna be performed. These are the tools that are available for this step: {{ definitions}}
		[/INST]
		The user input is:
		<s> {{ message}}
		</s>
		
		[INST]
		If a tool call can be inferred according to Json Schema directly send a valid json object without any additional content.
		Don't include any kind of introductory comment or syntax no backticks (```) just the valid json object that was inferred in the following format:
		{ "tool": { "name": "tool_name", "parameters": { "parameter_name": "parameter_value" } } }
		
		[/INST]
		"""
        )

    def __load__(self):
        return AsyncClient()

    async def chat(self, message: str) -> AsyncIterator[str]:
        """Send a message to the agent and return the response."""
        self.messages.append(Message(role="user", content=message))
        response = await self.__load__().chat(
            model=self.model,
            stream=True,
            messages=[m.model_dump() for m in self.messages],  # type: ignore
        )
        assert isinstance(response, AsyncIterator)
        string = ""
        async for choice in response:
            content = choice["message"].get("content")
            if content and isinstance(content, str):
                string += content
                yield content
        self.messages.append(Message(role="assistant", content=string))

    async def run(self, message: str):
        string = ""
        async for response in self.chat(
            self.template.render(
                message=message,
                definitions=[klass.definition() for klass in self.tools],
            )
        ):
            if response:
                string += response
        data = json.loads(string)
        tool = next(
            klass(**data["tool"]["parameters"])
            for klass in self.tools
            if klass.__name__ == data["tool"]["name"]
        )
        return await tool.run()
