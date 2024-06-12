from ..config import Configuration
from typing import Optional, Union
import importlib

from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.contracts.TextEmbedder import TextEmbedder


class ModelLoader:
    """
    Loads models from the model garden based on configuration.
    """

    _loaded_models: dict = {}  # Type hint for dictionary

    @classmethod
    def load_model(cls, model_name: str) -> Union[TextGenerator, TextEmbedder]:
        """
        Loads a model from the model garden based on the given model name.

        Args:
            model_name (str): The name of the model to load.

        Returns:
            Union[TextGenerator, TextEmbedder]: The loaded model object.

        Raises:
            ValueError: If the model with the given name is not found in the model garden.
        """

        if cls._is_model_exists(model_name):
            return cls._get_model(model_name)

        model_garden = Configuration.get("model_garden")
        model_info = model_garden.get(model_name)
        if not model_info:
            raise ValueError(f"Model {model_name} not found in the model garden.")

        model_path = model_info["path"]
        class_name = model_info["name"]
        params = model_info.get("params", {})

        model = cls._load_model(model_path, class_name, params)
        cls._store_model(model_name, model)
        return model

    @staticmethod
    def _load_model(
            model_path: str, class_name: str, params: Optional[dict] = None
    ) -> Union[TextGenerator, TextEmbedder]:
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

    @classmethod
    def _get_model(cls, model_name: str) -> Union[TextGenerator, TextEmbedder]:
        """
        Gets a model from the loaded_models dictionary based on the given model name.

        Args:
            model_name (str): The name of the model to get.

        Returns:
            Union[TextGenerator, TextEmbedder]: The loaded model object.

        Raises:
            ValueError: If the model with the given name is not found in the loaded_models dictionary.
        """

        if not cls._is_model_exists(model_name):
            raise ValueError(f"Model {model_name} not found in the loaded_models dictionary.")
        return cls._loaded_models[model_name]

    @classmethod
    def _store_model(cls, model_name: str, model: Union[TextGenerator, TextEmbedder]) -> None:
        """
        Stores a model in the loaded_models dictionary based on the given model name.

        Args:
            model_name (str): The name of the model to store.
            model (Union[TextGenerator, TextEmbedder]): The model to store.

        Returns:
            None
        """

        cls._loaded_models[model_name] = model

    @classmethod
    def _is_model_exists(cls, model_name: str) -> bool:
        """
        Checks if a model with the given name exists in the loaded_models dictionary.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model exists, False otherwise.
        """

        return model_name in cls._loaded_models
