import unittest
from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder

load_dotenv(override=True)
Configuration(path="configuration.yaml")

class TestDocumentEmbedder(unittest.TestCase):
    _instance: DocumentEmbedder = None

    @classmethod
    def setUpClass(cls) -> None:
        cls._instance = DocumentEmbedder()

    def test_instance_init(self):
        self.assertIsInstance(self._instance, DocumentEmbedder)
