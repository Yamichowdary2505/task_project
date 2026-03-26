from google import genai
from langchain_core.language_models import LLM
from dotenv import load_dotenv
from typing import Optional, List
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

class GeminiLLM(LLM):
    model: str = "gemini-2.5-flash"
    temperature: float = 0.9

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text

    @property
    def _identifying_params(self):
        return {"model": self.model, "temperature": self.temperature}

    @property
    def _llm_type(self) -> str:
        return "gemini"
