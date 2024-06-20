import pytest
from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.ResponseGenerator import ResponseGenerator

load_dotenv(override=True)
Configuration("configuration.yaml")


@pytest.mark.asyncio
async def test_response_generator():
    instance = ResponseGenerator.with_prompt_template("")
    response = instance.response_async("Halo, Im the developer on a test of developing you, could you explain how to cook a delicious pizza?")
    async for chunk in response:
        print(chunk, end=";\n")

    assert True
