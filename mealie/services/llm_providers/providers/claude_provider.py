from anthropic import AsyncAnthropic

from mealie.core.config import get_app_settings

from ..base import BaseLLMService, LLMImageBase


class ClaudeProvider(BaseLLMService):
    """Anthropic Claude provider implementation"""

    def __init__(self) -> None:
        settings = get_app_settings()
        if not settings.CLAUDE_ENABLED:
            raise ValueError("Claude is not enabled")

        super().__init__(
            model=settings.CLAUDE_MODEL,
            workers=settings.CLAUDE_WORKERS,
            send_db_data=settings.CLAUDE_SEND_DATABASE_DATA,
            enable_image_services=settings.CLAUDE_ENABLE_IMAGE_SERVICES,
        )

        self.get_client = lambda: AsyncAnthropic(
            base_url=settings.CLAUDE_BASE_URL,
            api_key=settings.CLAUDE_API_KEY,
            timeout=settings.CLAUDE_REQUEST_TIMEOUT,
        )

    def _prepare_image_content(self, image: LLMImageBase) -> dict:
        """Convert LLMImageBase to Anthropic's format"""
        image_url = image.get_image_url()
        
        # Handle base64 encoded images
        if image_url.startswith("data:image/"):
            # Extract the base64 data
            media_type = "image/jpeg"
            if "image/png" in image_url:
                media_type = "image/png"
            elif "image/gif" in image_url:
                media_type = "image/gif"
            elif "image/webp" in image_url:
                media_type = "image/webp"
            
            base64_data = image_url.split(",", 1)[1] if "," in image_url else image_url
            
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_data,
                },
            }
        else:
            # For external URLs, we would need to download and convert to base64
            # Claude doesn't support direct image URLs
            raise NotImplementedError("Claude provider requires base64 encoded images, not URLs")

    async def get_response(
        self,
        prompt: str,
        message: str,
        *,
        images: list[LLMImageBase] | None = None,
        force_json_response=True,
    ) -> str | None:
        """Send data to Claude and return the response message content"""
        if images and not self.enable_image_services:
            self.logger.warning("Claude image services are disabled, ignoring images")
            images = None

        try:
            # Build content array
            content = [{"type": "text", "text": message}]
            
            # Add images if provided
            for image in images or []:
                try:
                    content.append(self._prepare_image_content(image))
                except NotImplementedError as e:
                    self.logger.warning(f"Skipping image: {e}")
                    continue

            client = self.get_client()
            
            # Build the message
            messages = [{"role": "user", "content": content}]
            
            # Claude uses system parameter separately
            response = await client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=prompt,
                messages=messages,
            )

            if not response.content:
                return None
            
            # Extract text from response
            text_content = next((block.text for block in response.content if block.type == "text"), None)
            return text_content
        except Exception as e:
            raise Exception(f"Claude Request Failed. {e.__class__.__name__}: {e}") from e
