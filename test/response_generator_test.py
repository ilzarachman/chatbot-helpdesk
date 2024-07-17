import pytest
from dotenv import load_dotenv
import asyncio

from chatbot.config import Configuration
from chatbot.dependencies.ResponseGenerator import ResponseGenerator

load_dotenv(override=True)
Configuration("configuration.yaml")


@pytest.mark.asyncio(scope="session")
async def test_response_generator():
    instance = ResponseGenerator.with_prompt_template("")
    response = instance.response_async(
        "Halo, Im the developer on a test of developing you, could you explain how to cook a delicious pizza?",
        [],
    )
    chunks = []
    async for chunk in response:
        print(chunk, end=";\n")
        chunks.append(chunk)

    # Perform meaningful assertions
    assert chunks  # Ensure chunks are not empty
    assert all(
        isinstance(chunk, str) for chunk in chunks
    )  # Ensure all chunks are strings
    assert any(
        "pizza" in chunk.lower() for chunk in chunks
    )  # Ensure at least one chunk mentions "pizza"
