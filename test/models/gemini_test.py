from typing import Generator
import unittest
from chatbot.config import Configuration
from chatbot.dependencies.language_models.Gemini import Gemini

class TestGemini(unittest.TestCase):
    _instance = None

    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        cls._instance = Gemini()
        return super().setUpClass()
    
    def test_generate_text(self):
        text = self._instance.generate("This is a prompt.")
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)
    
    def test_streaming_text_returns_generator(self):
        generator = self._instance.stream("This is a prompt.")
        self.assertIsInstance(generator, Generator)
    