from openai import NOT_GIVEN, AsyncOpenAI
from openai.types.chat import ChatCompletion

from mealie.core.config import get_app_settings

from ..base import BaseLLMService, LLMImageBase


class OpenAIProvider(BaseLLMService):
    """OpenAI provider implementation"""

    def __init__(self) -> None:
        settings = get_app_settings()
        if not settings.OPENAI_ENABLED:
            raise ValueError("OpenAI is not enabled")

        super().__init__(
            model=settings.OPENAI_MODEL,
            workers=settings.OPENAI_WORKERS,
            send_db_data=settings.OPENAI_SEND_DATABASE_DATA,
            enable_image_services=settings.OPENAI_ENABLE_IMAGE_SERVICES,
        )

        self.get_client = lambda: AsyncOpenAI(
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_REQUEST_TIMEOUT,
            default_headers=settings.OPENAI_CUSTOM_HEADERS,
            default_query=settings.OPENAI_CUSTOM_PARAMS,
        )

    async def _get_raw_response(self, prompt: str, content: list[dict], force_json_response=True) -> ChatCompletion:
        client = self.get_client()
        return await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            model=self.model,
            response_format={"type": "json_object"} if force_json_response else NOT_GIVEN,
        )

    async def get_response(
        self,
        prompt: str,
        message: str,
        *,
        images: list[LLMImageBase] | None = None,
        force_json_response=True,
    ) -> str | None:
        """Send data to OpenAI and return the response message content"""
        if images and not self.enable_image_services:
            self.logger.warning("OpenAI image services are disabled, ignoring images")
            images = None

        try:
            user_messages = [{"type": "text", "text": message}]
            for image in images or []:
                user_messages.append(image.build_message())

            response = await self._get_raw_response(prompt, user_messages, force_json_response)
            if not response.choices:
                return None
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI Request Failed. {e.__class__.__name__}: {e}") from e
