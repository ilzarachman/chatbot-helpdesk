from typing import Optional
from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.utils.StringEnum import StringEnum


class Intent(StringEnum):
    RELEVANT = "relevan"
    NOT_RELEVANT = "tidak_relevan"

    @staticmethod
    def list() -> list[str]:
        """
        Helper method to load the intents from the intent classifier config.

        Returns:
            list[str]: A list of intents.
        """
        _intents = []
        for intent in Intent:
            _intents.append(intent.value)
        return _intents


class IntentClassifier:
    """
    This class is used to classify the intent of a message.
    """

    def __init__(self):
        """
        Initializes an instance of the IntentClassifier class.
        """
        self._intent_classifier_config: dict = Configuration.get("intent_classifier")
        self._model: TextGenerator = self._load_model()
        self._prompt_template: str = self._get_prompt_template()

    @staticmethod
    def _get_prompt_template() -> str:
        """
        Helper method to get the prompt template.

        Returns:
            str: The prompt template.
        """
        intents: str = ", ".join(Intent.list())
        return PromptManager.get_prompt(
            "intent_classification", "main_prompt", {"intent_list": intents}
        )

    def _load_model(self) -> TextGenerator:
        """
        Helper method to load the Generator model.

        Returns:
            TextGenerator: The loaded model object.
        """
        _model_name: str = self._intent_classifier_config.get("model")
        return ModelLoader.load_model(_model_name)

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
