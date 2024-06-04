from typing import Optional, Union
import importlib
from chatbot.dependencies.contracts.TextEmbedder import TextEmbedder
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from .dependencies.IntentClassifier import IntentClassifier
from .dependencies.DocumentEmbedder import DocumentEmbedder
from .dependencies.InformationRetriever import InformationRetriever
from .dependencies.ResponseGenerator import ResponseGenerator
from .logger import logger
from .config import Configuration

class Application:
    """
    This class represents the main application that integrates all the components of the chatbot.
    It provides a single point of access to the chatbot's functionality.
    """

    _instance: Optional["Application"] = None

    def __init__(self):
        """
        Initialize the application.
        """
        self.intent_classifier = IntentClassifier()
        self.document_embedder = DocumentEmbedder()
        self.information_retriever = InformationRetriever()
        self.response_generator = ResponseGenerator()

        # NOTE: Below code is just for testing purposes.
        model = self.load_model("gemini")
        for chunk in model.stream("Explain me about FastAPI python!"):
            print(chunk)

        logger.info("Application initialized successfully!")
    
    def load_model(self, model_name: str, params: dict = {}) -> Union[TextGenerator, TextEmbedder]:
        """
        Loads a model from the model garden based on the given model name.

        Args:
            model_name (str): The name of the model to load.
            params (dict): Additional parameters to pass to the model constructor.

        Returns:
            Union[TextGenerator, TextEmbedder]: The loaded model object.

        Raises:
            ValueError: If the model with the given name is not found in the model garden.
        """
        model_garden = Configuration.get("model_garden")
        model_info = model_garden.get(model_name)
        if model_info:
            model_path = model_info["path"]
            class_name = model_info["name"]
            module = importlib.import_module(model_path)
            model_class = getattr(module, class_name)
            model = model_class(**params)
            return model

        raise ValueError(f"Model {model_name} not found in the model garden.")


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Application":
        """
        Get the instance of the application.

        Returns:
            Application: The instance of the application.
        """
        if not cls._instance:
            cls._instance = Application()
        return cls._instance
