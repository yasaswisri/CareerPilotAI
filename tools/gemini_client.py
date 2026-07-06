import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt):
    """Call Gemini and return a friendly fallback message if the service is rate-limited."""
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
        return "The Gemini service is temporarily unavailable. Please try again shortly."
    except Exception:
        return "I could not reach the Gemini service right now. Please try again shortly."