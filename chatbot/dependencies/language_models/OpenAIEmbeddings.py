from langchain_openai import OpenAIEmbeddings as LangChainOpenAIEmbeddings

from ..contracts.TextEmbedder import TextEmbedder


class OpenAIEmbeddings(TextEmbedder):

    def __init__(self, model_name: str = "text-embedding-3-large"):
        """
        Initializes the OpenAIEmbeddings object.

        Args:
            model_name (str): The name of the model to use for embeddings.

        Returns:
            None
        """
        self._model = LangChainOpenAIEmbeddings(model=model_name)

    @property
    def model(self) -> LangChainOpenAIEmbeddings:
        """
        Get the internal model.
        """
        return self._model

    def get_embedding(self, text: str) -> list[float]:
        """
        Embed a text into a vector.

        Args:
            text (str): The text to be embedded.

        Returns:
            Any
        """
        return self._model.embed_query(text)
