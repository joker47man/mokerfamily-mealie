import base64
import inspect
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent

from pydantic import BaseModel, field_validator

from mealie.pkgs import img

from .._base_service import BaseService


class LLMDataInjection(BaseModel):
    description: str
    value: str

    @field_validator("value", mode="before")
    def parse_value(cls, value):
        if not value:
            raise ValueError("Value cannot be empty")
        if isinstance(value, str):
            return value

        # convert Pydantic models to JSON
        if isinstance(value, BaseModel):
            return value.model_dump_json()

        # convert Pydantic types to their JSON schema definition
        if inspect.isclass(value) and issubclass(value, BaseModel):
            value = value.model_json_schema()

        # attempt to convert object to JSON
        try:
            return json.dumps(value, separators=(",", ":"))
        except TypeError:
            return value


class LLMImageBase(BaseModel, ABC):
    @abstractmethod
    def get_image_url(self) -> str: ...

    def build_message(self) -> dict:
        return {
            "type": "image_url",
            "image_url": {"url": self.get_image_url()},
        }


class LLMImageExternal(LLMImageBase):
    url: str

    def get_image_url(self) -> str:
        return self.url


class LLMLocalImage(LLMImageBase):
    filename: str
    path: Path

    def get_image_url(self) -> str:
        image = img.PillowMinifier.to_jpg(
            self.path, dest=self.path.parent.joinpath(f"{self.filename}-min-original.jpg")
        )
        with open(image, "rb") as f:
            b64content = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64content}"


class BaseLLMService(BaseService, ABC):
    """Abstract base class for LLM service providers"""

    PROMPTS_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "prompts"

    def __init__(self, model: str, workers: int = 1, send_db_data: bool = True, enable_image_services: bool = True) -> None:
        self.model = model
        self.workers = workers
        self.send_db_data = send_db_data
        self.enable_image_services = enable_image_services
        super().__init__()

    @classmethod
    def get_prompt(cls, name: str, data_injections: list[LLMDataInjection] | None = None) -> str:
        """
        Load stored prompt and inject data into it.

        Access prompts with dot notation.
        For example, to access `prompts/recipes/parse-recipe-ingredients.txt`, use
        `recipes.parse-recipe-ingredients`
        """

        if not name:
            raise ValueError("Prompt name cannot be empty")

        tree = name.split(".")
        prompt_dir = os.path.join(cls.PROMPTS_DIR, *tree[:-1], tree[-1] + ".txt")
        try:
            with open(prompt_dir) as f:
                content = f.read()
        except OSError as e:
            raise OSError(f"Unable to load prompt {name}") from e

        if not data_injections:
            return content

        content_parts = [content]
        for data_injection in data_injections:
            content_parts.append(
                dedent(
                    f"""
                    ###
                    {data_injection.description}
                    ---

                    {data_injection.value}
                    """
                )
            )
        return "\n".join(content_parts)

    @abstractmethod
    async def get_response(
        self,
        prompt: str,
        message: str,
        *,
        images: list[LLMImageBase] | None = None,
        force_json_response: bool = True,
    ) -> str | None:
        """Send data to LLM provider and return the response message content"""
        ...
