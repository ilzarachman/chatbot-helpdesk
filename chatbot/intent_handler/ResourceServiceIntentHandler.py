from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class ResourceServiceIntentHandler(BaseIntentHandler):
    """
    Intent handler for Support Service intent.
    """

    def __init__(self):
        super().__init__()
        self._intent: Intent = Intent.RESOURCE_SERVICE
        self.with_prompt_template(self._intent)
