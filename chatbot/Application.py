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
        self.loaded_models = {}  # Dictionary to store loaded models
        
        self.intent_classifier = IntentClassifier()
        self.document_embedder = DocumentEmbedder()
        self.information_retriever = InformationRetriever()
        self.response_generator = ResponseGenerator()

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
        # Check if the model is already loaded in the loaded_models dictionary
        if self._is_model_exists(model_name):
            return self._get_model(model_name)
        
        model_garden: dict = Configuration.get("model_garden")
        model_info = model_garden.get(model_name)
        if model_info:
            model_path: str = model_info["path"]
            class_name: str = model_info["name"]
            model = self._load_model(model_path, class_name, params)
            self._store_model(model_name, model)    # Store the model in the loaded_models dictionary
            return model

        raise ValueError(f"Model {model_name} not found in the model garden.")
    
    def _load_model(self, model_path: str, class_name: str, params: dict = {}) -> Union[TextGenerator, TextEmbedder]:
        """
        Actually loads a model from the model garden based on the given model path and class name.
        
        Args:
            model_path (str): The path to the model module.
            class_name (str): The name of the model class.
            params (dict): Additional parameters to pass to the model constructor.
        
        Returns:
            Union[TextGenerator, TextEmbedder]: The loaded model object.
        """
        module = importlib.import_module(model_path)
        model_class = getattr(module, class_name)
        model = model_class(**params)
        return model
    
    def _get_model(self, model_name: str) -> Union[TextGenerator, TextEmbedder]:
        """
        Gets a model from the loaded_models dictionary based on the given model name.

        Args:
            model_name (str): The name of the model to get.

        Returns:
            Union[TextGenerator, TextEmbedder]: The loaded model object.

        Raises:
            ValueError: If the model with the given name is not found in the loaded_models dictionary.
        """
        if not self._is_model_exists(model_name):
            raise ValueError(f"Model {model_name} not found in the loaded_models dictionary.")
        return self.loaded_models[model_name]
    
    def _store_model(self, model_name: str, model: Union[TextGenerator, TextEmbedder]) -> None:
        """
        Stores a model in the loaded_models dictionary based on the given model name.

        Args:
            model_name (str): The name of the model to store.
            model (Union[TextGenerator, TextEmbedder]): The model to store.

        Returns:
            None
        """
        self.loaded_models[model_name] = model
    
    def _is_model_exists(self, model_name: str) -> bool:
        """
        Checks if a model with the given name exists in the loaded_models dictionary.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model exists, False otherwise.
        """
        return model_name in self.loaded_models


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
