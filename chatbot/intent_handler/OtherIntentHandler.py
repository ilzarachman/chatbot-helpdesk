from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class OtherIntentHandler(BaseIntentHandler):
    """
    Intent handler for other intent.
    """

    async def handle(self, message: str) -> str:
        """
        Handles the intent of the message.

        This function takes a message as input and returns the response as a string.

        Parameters:
            message (str): The message to be handled.

        Returns:
            str: The response to the message.
        """
        return "Dukungan Lainnya"
