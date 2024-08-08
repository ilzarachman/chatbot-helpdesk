from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class SupportIntentHandler(BaseIntentHandler):
    """
    Intent handler for Support intent.
    """

    def __init__(self):
        super().__init__()
        self._intent: Intent = Intent.SUPPORT
        self.with_prompt_template(self._intent)
