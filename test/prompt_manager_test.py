import unittest

from chatbot.config import Configuration
from chatbot.dependencies.PromptManager import PromptManager


class TestPromptManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Configuration(path="configuration.yaml")
        return super().setUpClass()

    def test_get_prompt_returns_string(self):
        prompt = PromptManager.get_prompt("intent_classification", "main_prompt")
        self.assertIsInstance(prompt, str)
