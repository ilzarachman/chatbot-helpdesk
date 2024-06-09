import os
from typing import Generator
import unittest
from dotenv import load_dotenv
from chatbot.config import Configuration
from chatbot.dependencies.contracts.message import AssistantMessage, Message, UserMessage
from chatbot.dependencies.language_models.Gemini import Gemini


class TestGemini(unittest.TestCase):
    _instance = None

    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        load_dotenv(override=True)
        cls._instance = Gemini()
        return super().setUpClass()

    def test_generate_text(self):
        text = self._instance.generate([UserMessage("This is a prompt.")])
        print(text)
        self.assertIsNotNone(text)
        self.assertIsInstance(text, str)

    @unittest.skip("Because of long runtime.")
    def test_streaming_text_returns_generator(self):
        generator = self._instance.stream([Gemini.GeminiUserMessage("This is a prompt.")])
        self.assertIsInstance(generator, Generator)

    def test_message_template_casts_to_str(self):
        user_message = Gemini.GeminiUserMessage("This is a prompt.")
        assistant_message = Gemini.GeminiAssistantMessage("This is an answer.")
        self.assertIsInstance(user_message, Message)
        self.assertIsInstance(assistant_message, Message)
        self.assertIsInstance(str(user_message), str)
        self.assertIsInstance(str(assistant_message), str)
