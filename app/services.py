from typing import List, Tuple
import requests
from openai import OpenAI
from google.cloud import texttospeech
from .models import NewsBriefing
from .config import Settings
import logging
import os

logger = logging.getLogger(__name__)

async def get_news_articles(max_articles: int, settings: Settings) -> List[dict]:
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": settings.NEWS_API_KEY,
            "category": "technology",
            "language": "en",
            "pageSize": max_articles
        }
        
        logger.info(f"Fetching news articles from {url}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json()["articles"]
        logger.info(f"Successfully fetched {len(articles)} articles")
        return articles
    except Exception as e:
        logger.error(f"Error fetching news articles: {str(e)}", exc_info=True)
        raise

async def create_batch_summary(articles: List[dict], summary_length: str, settings: Settings) -> str:
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        articles_text = "\n\n".join([
            f"Title: {article['title']}\n"
            f"Content: {article['content'] or article['description']}"
            for article in articles
        ])
        
        max_tokens = {
            "short": 150,
            "medium": 250,
            "long": 350
        }.get(summary_length, 150)
        
        logger.info(f"Creating summary with length {summary_length}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"""
                Please provide a {summary_length} summary of today's tech news, based on these articles:
                
                {articles_text}
                
                Create a coherent, conversational summary that connects the main themes and developments.
                Keep it engaging and suitable for text-to-speech.
                """
            }],
            max_tokens=max_tokens,
            temperature=0.7,
            presence_penalty=0.0,
            frequency_penalty=0.0
        )
        summary = response.choices[0].message.content
        logger.info("Successfully created summary")
        return summary
    except Exception as e:
        logger.error(f"Error creating summary: {str(e)}", exc_info=True)
        raise

async def text_to_speech(text: str, settings: Settings) -> bytes:
    try:
        logger.info("Initializing Text-to-Speech client")
        # Set credentials explicitly
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        logger.info("Generating speech")
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        logger.info("Successfully generated speech")
        return response.audio_content
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}", exc_info=True)
        raise

async def test_google_credentials():
    logger.info(f"Checking GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
    try:
        client = texttospeech.TextToSpeechClient()
        voices = client.list_voices()
        logger.info("Successfully connected to Google Cloud TTS")
        return True
    except Exception as e:
        logger.error(f"Google Cloud TTS credential error: {str(e)}", exc_info=True)
        return False

async def test_openai_api():
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        logger.info("OpenAI API test successful")
        return True
    except Exception as e:
        logger.error(f"OpenAI API test failed: {str(e)}")
        return False

async def get_news_briefing(max_articles: int, summary_length: str, settings: Settings) -> dict:
    # Adjust number of articles based on summary length
    articles_count = {
        "short": 5,
        "medium": 10,
        "long": 15
    }.get(summary_length, 5)
    
    # Test APIs first
    await test_google_credentials()
    await test_openai_api()
    
    articles = await get_news_articles(articles_count, settings)  # Use adjusted count
    summary = await create_batch_summary(articles, summary_length, settings)
    audio = await text_to_speech(summary, settings)
    
    return {
        "summary": summary,
        "audio_content": audio
    } 