from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import logging
from io import BytesIO
from . import services
from .models import NewsBriefing
from .config import get_settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")

@router.get("/briefing/")
async def get_tech_news_briefing(
    max_articles: Optional[int] = 5,
    summary_length: Optional[str] = "short",
    settings = Depends(get_settings)
):
    try:
        logger.info(f"Starting news briefing request: max_articles={max_articles}, summary_length={summary_length}")
        briefing = await services.get_news_briefing(max_articles, summary_length, settings)
        logger.info("Successfully generated briefing")
        return {
            "summary": briefing["summary"],
            "audio_content": {"data": list(briefing["audio_content"])}  # Convert bytes to list for JSON serialization
        }
    except Exception as e:
        logger.error(f"Error in get_tech_news_briefing: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"Service temporarily unavailable. Error: {str(e)}"
        )

@router.get("/briefing/audio/")
async def get_audio(
    summary: str,
    settings = Depends(get_settings)
):
    try:
        logger.info("Starting audio generation")
        audio = await services.text_to_speech(summary, settings)
        logger.info("Successfully generated audio")
        return StreamingResponse(
            BytesIO(audio),
            media_type="audio/mpeg"
        )
    except Exception as e:
        logger.error(f"Error in get_audio: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail=f"Audio generation failed. Error: {str(e)}"
        ) 