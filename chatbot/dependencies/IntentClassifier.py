from typing import Optional
from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextGenerator import TextGenerator


class IntentClassifier:
    def __init__(self):
        self._intent_classifier_config: dict = Configuration.get("intent_classifier")
        _model_name = self._intent_classifier_config.get("model")
        self._model: Optional[TextGenerator] = ModelLoader.load_model(_model_name)

    def classify(self, message: str) -> str:
        """Classify the intent of the given message.

        This function takes a message as input and returns the intent of the message as a string.

        Parameters:
            message (str): The message to be classified.

        Returns:
            str: The intent of the message.
        """
        # TODO: Add classify implementation in here
        pass
