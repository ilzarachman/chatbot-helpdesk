import unittest

from chatbot.config import Configuration
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.IntentClassifier import Intent
from dotenv import load_dotenv

from chatbot.logger import logger, configure_logging

load_dotenv(override=True)
Configuration(path="configuration.yaml")
configure_logging()


class TestInformationRetriever(unittest.TestCase):
    _instance: InformationRetriever = None

    @classmethod
    def setUpClass(cls):
        cls._instance = InformationRetriever()

    def test_instance(self):
        self.assertIsInstance(self._instance, InformationRetriever)

    def test_retrieve_returns_string(self):
        self.assertIsInstance(
            self._instance.retrieve("who is Mrs Shears?", Intent.ACADEMIC_ADMINISTRATION), str
        )
