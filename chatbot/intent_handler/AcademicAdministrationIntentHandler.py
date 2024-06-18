from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class AcademicAdministrationIntentHandler(BaseIntentHandler):
    """
    Intent handler for Academic Administration intent.
    """

    _intent: Intent = Intent.ACADEMIC_ADMINISTRATION

    def __init__(self):
        super().__init__()
        self.with_prompt_template(self._intent)

    async def handle(self, message: str) -> str:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        # 1. search for information in FAISS index
        information = self.application.information_retriever.retrieve(
            message, self._intent
        )
        # 2. generate the prompt template
        prompt_template = self.build_prompt_with_information(information)
        # 3. generate the response
        response_generator = ResponseGenerator.with_prompt_template(prompt_template)
        response = await response_generator.response_async(message)

        return response
