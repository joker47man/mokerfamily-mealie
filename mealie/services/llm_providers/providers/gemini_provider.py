import json

import google.generativeai as genai

from mealie.core.config import get_app_settings

from ..base import BaseLLMService, LLMImageBase


class GeminiProvider(BaseLLMService):
    """Google Gemini provider implementation"""

    def __init__(self) -> None:
        settings = get_app_settings()
        if not settings.GEMINI_ENABLED:
            raise ValueError("Gemini is not enabled")

        super().__init__(
            model=settings.GEMINI_MODEL,
            workers=settings.GEMINI_WORKERS,
            send_db_data=settings.GEMINI_SEND_DATABASE_DATA,
            enable_image_services=settings.GEMINI_ENABLE_IMAGE_SERVICES,
        )

        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        self.timeout = settings.GEMINI_REQUEST_TIMEOUT

    def _prepare_image_content(self, image: LLMImageBase):
        """Convert LLMImageBase to Gemini's format"""
        import base64
        from PIL import Image
        import io

        image_url = image.get_image_url()
        
        # Handle base64 encoded images
        if image_url.startswith("data:image/"):
            # Extract the base64 data
            base64_data = image_url.split(",", 1)[1] if "," in image_url else image_url
            image_bytes = base64.b64decode(base64_data)
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            return pil_image
        else:
            # For external URLs, Gemini supports them directly
            return image_url

    async def get_response(
        self,
        prompt: str,
        message: str,
        *,
        images: list[LLMImageBase] | None = None,
        force_json_response=True,
    ) -> str | None:
        """Send data to Gemini and return the response message content"""
        if images and not self.enable_image_services:
            self.logger.warning("Gemini image services are disabled, ignoring images")
            images = None

        try:
            # Combine system prompt with user message
            full_message = f"{prompt}\n\n{message}"
            
            # Build content array
            content = [full_message]
            
            # Add images if provided
            for image in images or []:
                try:
                    content.append(self._prepare_image_content(image))
                except Exception as e:
                    self.logger.warning(f"Skipping image: {e}")
                    continue

            # Create model instance
            generation_config = {
                "temperature": 0.4,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
            }
            
            if force_json_response:
                generation_config["response_mime_type"] = "application/json"

            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config=generation_config,
            )

            # Generate response
            response = await model.generate_content_async(content)

            if not response.text:
                return None
            
            return response.text
        except Exception as e:
            raise Exception(f"Gemini Request Failed. {e.__class__.__name__}: {e}") from e
