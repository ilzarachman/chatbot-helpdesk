from ..config import Configuration
from typing import Optional, Union
import importlib
from chatbot.dependencies.contracts.TextEmbedder import TextEmbedder
from chatbot.dependencies.contracts.TextGenerator import TextGenerator

class ModelLoader:
    _loaded_models = {}  # Dictionary to store loaded models

    def load_model(self, model_name: str) -> Union[TextGenerator, TextEmbedder]:
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
        if self._is_model_exists(model_name):
            return self._get_model(model_name)

        model_garden: dict = Configuration.get("model_garden")
        model_info: dict = model_garden.get(model_name)
        if model_info:
            model_path: str = model_info["path"]
            class_name: str = model_info["name"]
            params: dict = model_info.get("params", {})
            model = self._load_model(model_path, class_name, params)
            self._store_model(model_name, model)  # Store the model in the loaded_models dictionary
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
        return ModelLoader._loaded_models[model_name]

    def _store_model(self, model_name: str, model: Union[TextGenerator, TextEmbedder]) -> None:
        """
        Stores a model in the loaded_models dictionary based on the given model name.

        Args:
            model_name (str): The name of the model to store.
            model (Union[TextGenerator, TextEmbedder]): The model to store.

        Returns:
            None
        """
        ModelLoader._loaded_models[model_name] = model

    def _is_model_exists(self, model_name: str) -> bool:
        """
        Checks if a model with the given name exists in the loaded_models dictionary.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model exists, False otherwise.
        """
        return model_name in ModelLoader._loaded_models