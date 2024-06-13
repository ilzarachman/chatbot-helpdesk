import unittest
from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.utils.path_utils import project_path

load_dotenv(override=True)
Configuration(path="configuration.yaml")


class TestDocumentEmbedder(unittest.TestCase):
    _instance: DocumentEmbedder = None

    @classmethod
    def setUpClass(cls) -> None:
        cls._instance = DocumentEmbedder()

    def test_instance_init(self):
        self.assertIsInstance(self._instance, DocumentEmbedder)

    def test_save_document_to_vectorstore(self):
        self._instance.save_document_to_vectorstore(
            str(project_path("test", "data", "text.txt")),
            Intent.ACADEMIC_ADMINISTRATION,
        )
        faiss_dir_path = project_path("faiss", Intent.ACADEMIC_ADMINISTRATION.value + "_db")
        self.assertTrue(faiss_dir_path.exists())
