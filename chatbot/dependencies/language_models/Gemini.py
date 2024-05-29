from ..contracts.TextGenerator import TextGenerator
from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini(TextGenerator):
    def generate(self, text):
        return text