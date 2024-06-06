import unittest
from chatbot.Application import Application
from chatbot.config import Configuration
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.language_models.Gemini import Gemini

class TestApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        return super().setUpClass()
    
    def test_get_instance_returns_the_same_instance(self):
        instance1 = Application()
        instance2 = Application.get_instance()
        self.assertEqual(instance1, instance2)
    
    def test_reinitializes_the_instance_returns_the_same_instance(self):
        instance1 = Application()
        instance2 = Application()
        self.assertEqual(instance1, instance2)
    
    def test_load_model_returns_the_expected_model(self):
        app = Application()
        model = app.load_model("gemini")
        self.assertIsInstance(model, TextGenerator)
        self.assertIsInstance(model, Gemini)
    
    def test_load_model_raises_exception_when_model_not_found(self):
        app = Application()
        with self.assertRaises(ValueError):
            app.load_model("nonexistent_model")
