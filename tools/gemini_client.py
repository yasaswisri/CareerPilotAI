import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()


def _get_api_key():
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


api_key = _get_api_key()

if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None
else:
    client = None


def _is_key_issue(exc):
    message = str(exc).upper()
    return (
        "PERMISSION_DENIED" in message
        or "API_KEY" in message
        or "AUTH" in message
        or "INVALID" in message
        or "LEAKED" in message
    )


def ask_gemini(prompt):
    """Call Gemini and return a friendly fallback message for rate limits or misconfiguration."""
    if not api_key:
        return "Gemini is not configured yet. Please add a valid GOOGLE_API_KEY or GEMINI_API_KEY to your environment and restart the app."
    if client is None:
        return "The Gemini client could not be initialized. Please verify your API configuration and restart the app."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return getattr(response, "text", str(response))
    except ClientError as exc:
        message = str(exc).upper()
        if "RESOURCE_EXHAUSTED" in message or "429" in message:
            return "The Gemini API is currently rate-limited. Please try again in a moment."
        if _is_key_issue(exc):
            return "The Gemini API key appears to be invalid, expired, or blocked. Please add a new API key to your .env file and restart the app."
        return "The Gemini service is temporarily unavailable. Please try again shortly."
    except Exception:
        return "I could not reach the Gemini service right now. Please try again shortly."