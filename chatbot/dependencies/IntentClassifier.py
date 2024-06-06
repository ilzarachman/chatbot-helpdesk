from typing import Optional
from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.contracts.TextGenerator import TextGenerator


class IntentClassifier():
    def __init__(self):
        self.intent_classifier_config: dict = Configuration.get("intent_classifier")

    @property
    def model(self) -> TextGenerator:
        if not self._model:
            self._model = ModelLoader().load_model(self.intent_classifier_config.get("model"))
        return self._model

    def classify(self, message: str) -> str:
        """Classify the intent of the given message.

        This function takes a message as input and returns the intent of the message as a string.

        Parameters:
            message (str): The message to be classified.

        Returns:
            str: The intent of the message.
        """
        pass