import unittest

from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import IntentClassifier, Intent


class TestIntentClassifier(unittest.TestCase):
    _intent_classifier: IntentClassifier = None

    def setUp(self):
        Configuration(path="configuration.yaml")
        load_dotenv(override=True)
        self._intent_classifier = IntentClassifier()

    def test_intent_classifier(self):
        self.assertIsInstance(self._intent_classifier, IntentClassifier)

    def test_intent_list_returns_list(self):
        list_intents = Intent.list()
        self.assertIsInstance(list_intents, list)

    def test_classify_returns_intent_string(self):
        intent = self._intent_classifier.classify("apakah ada matkul biologi semester ini?")
        print(intent)
        self.assertIsInstance(intent, str)
