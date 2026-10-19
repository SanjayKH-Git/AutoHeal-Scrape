import os
import google.generativeai as genai
from config import LLM_PROVIDER, GOOGLE_API_KEY

if LLM_PROVIDER == "gemini":
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")  # fast + free tier friendly


def call_llm(prompt: str) -> str:
    """
    Unified LLM call (Gemini version)
    """
    try:
        if LLM_PROVIDER == "gemini":
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0
                }
            )

            return response.text.strip()

    except Exception as e:
        print("LLM call failed:", e)
        return ""