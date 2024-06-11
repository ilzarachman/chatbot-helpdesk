import unittest
from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.language_models.Gemini import Gemini


class TestModelLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        return super().setUpClass()

    def test_load_model_returns_text_generator(self):
        model_loader = ModelLoader()
        model = model_loader.load_model("gemini")
        self.assertIsInstance(model, TextGenerator)
        self.assertIsInstance(model, Gemini)

    def test_load_nonexistent_model(self):
        model_loader = ModelLoader()
        with self.assertRaises(ValueError):
            model_loader.load_model("nonexistent_model")
