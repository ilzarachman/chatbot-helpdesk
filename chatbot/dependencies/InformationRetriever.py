from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextEmbedder import TextEmbedder


class InformationRetriever:
    """
    This class is responsible for retrieving information from documents based on the intent of the message.

    This class takes a message as input and returns the relevant information from the documents as a string.

    It should be able to handle multiple documents and retrieve the relevant information from each one based on the intent of the message.
    """

    def __init__(self):
        self._embedding_model: TextEmbedder = ModelLoader.load_model(
            Configuration.get("document_embedder.embedding_model")
        )
        pass

    def retrieve(self, message: str, intent: Intent) -> str:
        """Retrieve the relevant information from the documents based on the intent of the message.

        This function takes a message as input and returns the relevant information from the documents as a string.

        It should be able to handle multiple documents and retrieve the relevant information from each one based on the intent of the message.

        Parameters:
            message (str): The message to retrieve information based on.
            intent (str): The intent of the message.

        Returns:
            str: The relevant information from the documents based on the intent of the message.
        """
        # TODO: implement retrive function
        # 1. get the FAISS index based on the intent
        # 2. search the FAISS index for the relevant information
        # 3. return the relevant information
        pass
