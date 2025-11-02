import os
import shutil

from fastapi import APIRouter, File, UploadFile

from mealie.core.dependencies.dependencies import get_temporary_path
from mealie.routes._base import BaseAdminController, controller
from mealie.schema.admin.debug import DebugResponse
from mealie.services.llm_providers import (
    LLMLocalImage,
    get_active_provider_name,
    get_llm_service,
    is_llm_image_services_enabled,
    is_llm_provider_enabled,
)
from mealie.services.openai import OpenAILocalImage, OpenAIService

router = APIRouter(prefix="/debug")


@controller(router)
class AdminDebugController(BaseAdminController):
    @router.post("/openai", response_model=DebugResponse)
    async def debug_openai(self, image: UploadFile | None = File(None)):
        """Debug endpoint for LLM providers (maintained as /openai for backwards compatibility)"""
        
        if not is_llm_provider_enabled():
            return DebugResponse(success=False, response="No LLM provider is enabled")
        
        if image and not is_llm_image_services_enabled():
            return DebugResponse(
                success=False, response="Image was provided, but LLM image services are not enabled"
            )

        with get_temporary_path() as temp_path:
            if image:
                with temp_path.joinpath(image.filename).open("wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                local_image_path = temp_path.joinpath(image.filename)
                local_images = [LLMLocalImage(filename=os.path.basename(local_image_path), path=local_image_path)]
            else:
                local_images = None

            try:
                llm_service = get_llm_service()
                prompt = llm_service.get_prompt("debug")

                message = "Hello, checking to see if I can reach you."
                if local_images:
                    message = f"{message} Here is an image to test with:"

                response = await llm_service.get_response(
                    prompt, message, images=local_images, force_json_response=False
                )
                
                provider_name = get_active_provider_name() or "LLM"
                return DebugResponse(success=True, response=f'{provider_name} is working. Response: "{response}"')

            except Exception as e:
                self.logger.exception(e)
                return DebugResponse(
                    success=False,
                    response=f'LLM request failed. Full error has been logged. {e.__class__.__name__}: "{e}"',
                )
