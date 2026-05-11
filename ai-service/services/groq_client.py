from dotenv import load_dotenv
load_dotenv()
import os
import time
import logging
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FALLBACK_RESPONSE = {
    "result": "AI service is temporarily unavailable. Please try again shortly.",
    "is_fallback": True
}

def call_groq(messages: list, temperature: float = 0.3, max_tokens: int = 1000):
    """
    Call Groq API with retry logic.
    Returns the response text or fallback on failure.
    """
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content, False

        except Exception as e:
            logger.error(f"Groq API attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(2 ** attempt)  # backoff: 1s, 2s
            else:
                logger.error("All 3 Groq attempts failed, returning fallback")
                return FALLBACK_RESPONSE["result"], True