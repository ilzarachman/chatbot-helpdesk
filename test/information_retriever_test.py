import pytest
from chatbot.config import Configuration
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.IntentClassifier import Intent
from dotenv import load_dotenv
from chatbot.logger import logger, configure_logging

load_dotenv(override=True)
Configuration(path="configuration.yaml")
configure_logging()


_instance: InformationRetriever = InformationRetriever()


def test_instance():
    assert _instance is not None
    assert isinstance(_instance, InformationRetriever)


@pytest.mark.using_llm
@pytest.mark.asyncio(scope="session")
async def test_retrieve_returns_valid_response():
    response = await _instance.retrieve_async(
        "who is Mrs Shears?", Intent.ACADEMIC_ADMINISTRATION
    )

    # Ensure the response is a string
    assert isinstance(response, str)

    # Ensure the response is not empty
    assert response.strip() != "", "The response should not be empty"

    # Ensure the response contains expected keywords
    expected_keywords = ["mrs shears"]
    for keyword in expected_keywords:
        assert keyword in response.lower(), f"The response should contain the keyword '{keyword}'"

    # Ensure the response has a reasonable length
    assert len(response) > 20, "The response should be longer than 20 characters"


@pytest.mark.using_llm
@pytest.mark.asyncio(scope="session")
async def test_retrieve_public_returns_valid_response():
    response = await _instance.retrieve_public_async(
        "who is Mrs Shears?", Intent.ACADEMIC_ADMINISTRATION
    )

    # Ensure the response is a string
    assert isinstance(response, str)

    # Ensure the response is not empty
    assert response.strip() != "", "The response should not be empty"

    # Ensure the response contains expected keywords
    expected_keywords = ["mrs shears"]
    for keyword in expected_keywords:
        assert keyword in response.lower(), f"The response should contain the keyword '{keyword}'"

    # Ensure the response has a reasonable length
    assert len(response) > 20, "The response should be longer than 20 characters"
