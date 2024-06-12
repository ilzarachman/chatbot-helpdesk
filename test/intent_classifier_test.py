import unittest

import pytest
from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import IntentClassifier, Intent

load_dotenv(override=True)


class TestIntentClassifier(unittest.TestCase):
    _intent_classifier: IntentClassifier = None

    @classmethod
    def setUpClass(cls) -> None:
        Configuration(path="configuration.yaml")
        cls._intent_classifier = IntentClassifier()
        return super().setUpClass()

    def test_intent_classifier(self):
        self.assertIsInstance(self._intent_classifier, IntentClassifier)

    def test_intent_list_returns_list(self):
        list_intents = Intent.list()
        self.assertIsInstance(list_intents, list)

    @pytest.mark.generation
    def test_classify_returns_intent_other(self):
        intent = self._intent_classifier.classify("Halo, apa kabar?")
        self.assertEqual(intent, Intent.OTHER.value)

    @pytest.mark.generation
    def test_classify_returns_intent_academic(self):
        intent = self._intent_classifier.classify("Jurusan apa saja yang ada di kampus?")
        self.assertEqual(intent, Intent.ACADEMIC_ADMINISTRATION.value)

    @pytest.mark.generation
    def test_classify_returns_intent_resource(self):
        intent = self._intent_classifier.classify("Toilet kampus ada di mana?")
        self.assertEqual(intent, Intent.RESOURCE_SERVICE.value)

    @pytest.mark.generation
    def test_classify_returns_intent_support(self):
        intent = self._intent_classifier.classify("Saya mau melapor masalah dengan AC di ruangan 101.")
        self.assertEqual(intent, Intent.SUPPORT.value)
