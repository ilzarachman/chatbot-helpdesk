import pytest
from dotenv import load_dotenv

from chatbot.config import Configuration
from chatbot.dependencies.ResponseGenerator import ResponseGenerator

load_dotenv(override=True)
Configuration("configuration.yaml")


@pytest.mark.asyncio
async def test_response_generator():
    instance = ResponseGenerator.with_prompt_template("""Kamu adalah chatbot untuk membantu pertanyaan administrasi akademik.
  Berikan informasi atau instruksi yang jelas dan singkat berdasarkan permintaan pengguna.
  Jika permintaan tidak jelas, ajukan pertanyaan klarifikasi untuk lebih memahami kebutuhan pengguna.""")
    response = instance.response_async("Halo?")
    async for chunk in response:
        print(chunk)

    assert True
