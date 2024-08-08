import unittest

import pytest
from dotenv import load_dotenv
import asyncio

from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import IntentClassifier, Intent
import sys

from chatbot.logger import logger, configure_logging

load_dotenv(override=True)
Configuration(path="configuration.yaml")
configure_logging()

_intent_classifier: IntentClassifier = IntentClassifier()


def test_intent_classifier():
    assert isinstance(_intent_classifier, IntentClassifier)


def test_intent_list_returns_list():
    list_intents = Intent.list()
    assert isinstance(list_intents, list)


@pytest.mark.using_llm
@pytest.mark.generation
@pytest.mark.asyncio(scope="session")
async def test_classify_returns_intent_support():
    intent = await _intent_classifier.classify(
        "Saya mau melapor masalah dengan AC di ruangan 101."
    )
    assert intent == Intent.SUPPORT

    intent = await _intent_classifier.classify("Halo, apa kabar?")
    assert intent == Intent.OTHER

    intent = await _intent_classifier.classify("Toilet kampus ada di mana?")
    assert intent == Intent.RESOURCE_SERVICE

    intent = await _intent_classifier.classify("Jurusan apa saja yang ada di kampus?")
    assert intent == Intent.ACADEMIC_ADMINISTRATION
