import unittest
from chatbot.Application import Application
from chatbot.config import Configuration
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.language_models.Gemini import Gemini
from chatbot.dependencies.IntentClassifier import IntentClassifier
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.ResponseGenerator import ResponseGenerator

class TestApplication(unittest.TestCase):
    pass
    # _app = None

    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        TestApplication._app = Application(
            intent_classifier=IntentClassifier(),
            document_embedder=DocumentEmbedder(),
            information_retriever=InformationRetriever(),
            response_generator=ResponseGenerator(),
        )
        return super().setUpClass()

    def test_app_reinitialized_returns_the_same_instance(self):
        self.assertEqual(TestApplication._app, Application.get_instance())
    