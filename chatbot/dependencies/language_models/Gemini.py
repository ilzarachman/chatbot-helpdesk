import json
import os
import re
from contextlib import asynccontextmanager
from typing import Generator, Optional, Union, AsyncGenerator, AsyncIterator

from chatbot.dependencies.contracts.message import (
    AssistantMessage,
    UserMessage,
    Message,
    SystemMessage,
)
from chatbot.logger import logger
from ..contracts.TextGenerator import TextGenerator
import google.generativeai as genai
from google.generativeai import GenerationConfig
from google.generativeai.types import (
    generation_types,
    HarmCategory,
    HarmBlockThreshold,
    answer_types,
)


class Gemini(TextGenerator):
    """
    The Gemini class is a text generator that uses the LangChain Google Generative AI model to generate text.

    To use the Gemini class, first create an instance of the class:

    . code-block:: python
        gemini = Gemini()

    Then, call the `generate()` method with the text you want to generate:

    . code-block:: python
        text = gemini.generate("This is a prompt.")

    The `generate()` method will return the generated text.

    """

    class GeminiUserMessage(UserMessage):
        def __str__(self):
            return f"input: <MSG>{self.message}</MSG>"

    class GeminiAssistantMessage(AssistantMessage):
        def __str__(self):
            if not self.message:
                return f"output: <MSG>"
            return f"output: <MSG>{self.message}</MSG>"

    class GeminiSystemMessage(SystemMessage):
        def __str__(self):
            return f"system: <MSG>{self.message}</MSG>"

    class GeminiResponse:
        def __init__(self, response: str):
            self.response = re.sub(r"</MSG>", "", response)

        def __str__(self):
            return self.response

    def __init__(self, model_name: str = "gemini-1.0-pro"):
        harm_categories = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model_name, safety_settings=harm_categories)

    @staticmethod
    def _gemini_messages_to_str(messages: list[Message]) -> str:
        """
        Convert a list of messages to a string.

        Args:
            messages: The list of messages to convert.

        Returns:
            The string representation of the messages.
        """
        casted_messages: list[str] = []
        try:
            for MSG in messages:
                if isinstance(MSG, UserMessage):
                    casted_messages.append(str(Gemini.GeminiUserMessage(MSG.message)))
                elif isinstance(MSG, AssistantMessage):
                    casted_messages.append(
                        str(Gemini.GeminiAssistantMessage(MSG.message))
                    )
                elif isinstance(MSG, SystemMessage):
                    casted_messages.append(str(Gemini.GeminiSystemMessage(MSG.message)))

            casted_messages.append(str(Gemini.GeminiAssistantMessage(None)))
            return "\n".join([MSG for MSG in casted_messages])
        except Exception as e:
            logger.error(e)

    def _generate(
        self, prompt: str, config: GenerationConfig, **kwargs
    ) -> generation_types.GenerateContentResponse:
        """
        Generate text using the Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        try:
            res = self.model.generate_content(
                prompt, generation_config=config, **kwargs
            )
            return res
        except Exception as e:
            logger.error(e)
            raise RuntimeError("[Generation failed] " + str(e))

    async def _generate_async(
        self, prompt: str, config: GenerationConfig, **kwargs
    ) -> generation_types.AsyncGenerateContentResponse:
        """
        Generate text using the Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        try:
            res = await self.model.generate_content_async(
                prompt, generation_config=config, **kwargs
            )
            return res
        except Exception as e:
            logger.error(e)
            raise RuntimeError("[Generation failed] " + str(e))

    def generate(self, prompt: list[Message], config: Optional[dict] = None) -> str:
        """
        Generate text using the LangChain Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        config = GenerationConfig() if config is None else GenerationConfig(**config)
        prompt = self._gemini_messages_to_str(prompt)
        res = self._generate(prompt, config)
        try:
            res.resolve()
            text = Gemini.GeminiResponse(res.text)
            logger.debug(f"[Generated]: {text}")
            return str(text)
        except ValueError as e:
            logger.error(e)
            return self._handle_value_error(e, res)

    def stream(
        self, prompt: list[Message], config: Optional[dict] = None
    ) -> Generator[str, None, None]:
        """
        Generate text stream using the Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text stream.

        Raises:
            ValueError: If the response is not valid.
        """
        config = GenerationConfig() if config is None else GenerationConfig(**config)
        prompt = self._gemini_messages_to_str(prompt)
        res = self._generate(prompt, config, stream=True)
        try:
            for chunk in res:
                if "</MSG>" in chunk.text:
                    yield str(Gemini.GeminiResponse(chunk.text))
                    continue
                yield chunk.text
        except ValueError as e:
            logger.warning(e)
            yield self._handle_value_error(e, res)

    async def generate_async(
        self, prompt: list[Message], config: Optional[dict] = None
    ) -> str:
        """
        Generate text using the LangChain Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        config = GenerationConfig() if config is None else GenerationConfig(**config)
        prompt = self._gemini_messages_to_str(prompt)
        res = await self._generate_async(prompt, config)
        try:
            await res.resolve()
            text = Gemini.GeminiResponse(res.text)
            logger.debug(f"[Generated]: {text}")
            return str(text)
        except ValueError as e:
            logger.error(e)
            return self._handle_value_error(e, res)

    async def stream_async(
        self, prompt: list[Message], config: Optional[dict] = None
    ) -> AsyncIterator[str]:
        """
        Generate text stream using the Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text stream.

        Raises:
            ValueError: If the response is not valid.
        """
        config = GenerationConfig() if config is None else GenerationConfig(**config)
        prompt = self._gemini_messages_to_str(prompt)
        res = await self._generate_async(prompt, config, stream=True)
        try:
            async for chunk in res:
                if "</MSG>" in chunk.text:
                    yield str(Gemini.GeminiResponse(chunk.text))
                    continue
                yield chunk.text
        except ValueError as e:
            logger.warning(e)
            yield self._handle_value_error(e, res)

    @staticmethod
    def _handle_value_error(
        e: ValueError,
        response: Union[
            generation_types.GenerateContentResponse,
            generation_types.AsyncGenerateContentResponse,
        ],
    ) -> str:
        """
        Handle the ValueError exception.

        Args:
            response: The response from the Google Generative AI model.

        Returns:
            The error message.

        Raises:
            RuntimeError: If the response is not valid.
        """
        logger.warning(response.prompt_feedback)
        logger.warning(response.candidates[0].finish_reason)

        if response.candidates[0].finish_reason == answer_types.FinishReason.SAFETY:
            logger.warning(response.candidates[0].safety_ratings)
            return "Maaf, saya tidak dapat melakukan respon karena alasan keamanan."

        raise RuntimeError("[Generation failed] " + str(e))
