from ..contracts.TextGenerator import TextGenerator
from langchain_google_genai import ChatGoogleGenerativeAI

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
    def __init__(self, model_name: str = "gemini-1.0-pro", configuration: dict = None):
        self.model = ChatGoogleGenerativeAI(model_name)

    def generate(self, text: str) -> str:
        """
        Generates text using the LangChain Google Generative AI model.

        Args:
            text: The text to generate from.

        Returns:
            The generated text.

        """
        return self.model.generate(text)
    
    def stream(self, text: str) -> str:
        """
        Generates text using the LangChain Google Generative AI model.

        Args:
            text: The text to generate from.

        Returns:
            The generated text.

        """
        return self.model.stream(text)