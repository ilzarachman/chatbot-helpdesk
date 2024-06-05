from ctypes import Union
from typing import Generator, Optional

from chatbot.logger import logger
from ..contracts.TextGenerator import TextGenerator
import google.generativeai as genai
from google.generativeai import GenerationConfig 
from google.generativeai.types import generation_types, HarmCategory, HarmBlockThreshold, answer_types


class Gemini(TextGenerator):
    """
    The Gemini class is a text generator that uses the LangChain Google Generative AI model to generate text.

    To use the Gemini class, first create an instance of the class:

    .. code-block:: python
        gemini = Gemini()

    Then, call the `generate()` method with the text you want to generate:

    .. code-block:: python
        text = gemini.generate("This is a prompt.")

    The `generate()` method will return the generated text.

    """
    def __init__(self, model_name: str = "gemini-1.0-pro"):
        harm_categories = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        self.model = genai.GenerativeModel(model_name, safety_settings=harm_categories)
    
    def _generate(self, prompt: str, config: GenerationConfig, **kwargs) -> generation_types.GenerateContentResponse:
        """
        Generate text using the Google Generative AI model.
        
        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        try:
            res = self.model.generate_content(prompt, generation_config=config, **kwargs)
            return res
        except Exception as e:
            logger.error(e)
            raise RuntimeError("[Generation failed] " + str(e))

    def generate(self, prompt: str, config: Optional[dict] = None) -> str:
        """
        Generate text using the LangChain Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text.

        """
        try:
            config = GenerationConfig() if config is None else GenerationConfig(**config)
            res = self._generate(prompt, config)
            res.resolve()
            return res.text
        except ValueError as e:
            logger.warning(e)
            return self._handle_value_error(res)

    def stream(self, prompt: str, config: Optional[dict] = None) -> Generator[str, None, None]:
        """
        Generate text stream using the LangChain Google Generative AI model.

        Args:
            prompt: The text to generate from.
            config: The generation config.

        Returns:
            The generated text stream.

        Raises:
            ValueError: If the response is not valid.
        """
        try:
            config = GenerationConfig() if config is None else GenerationConfig(**config)
            res = self._generate(prompt, config, stream=True)
            for chunk in res:
                yield chunk.text
        except ValueError as e:
            logger.warning(e)
            return self._handle_value_error(res)
    
    def _handle_value_error(self, response: generation_types.GenerateContentResponse) -> str:
        """
        Handle the ValueError exception.

        Args:
            response: The response from the Google Generative AI model.

        Returns:
            The error message.

        Raises:
            RuntimeError: If the response is not valid.
        """
        logger.warn(response.prompt_feedback)
        logger.warn(response.candidates[0].finish_reason)
        
        if response.candidates[0].finish_reason == answer_types.FinishReason.SAFETY:
            logger.warn(response.candidates[0].safety_ratings)
            return "Maaf, saya tidak dapat melakukan respon karena alasan keamanan."
        
        raise RuntimeError("[Generation failed]")