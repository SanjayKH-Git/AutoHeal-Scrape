from google import genai
from google.genai import types
from config import LLM_PROVIDER, GOOGLE_API_KEY

client = None


def call_llm(prompt: str) -> str:
    """
    Unified LLM call (Gemini version)
    """
    try:
        if LLM_PROVIDER == "gemini":
            global client
            if client is None:
                client = genai.Client(api_key=GOOGLE_API_KEY)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0),
            )

            return (response.text or "").strip()

    except Exception as e:
        print("LLM call failed:", e)
        return ""