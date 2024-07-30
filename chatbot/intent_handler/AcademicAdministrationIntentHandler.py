from typing import AsyncIterator

from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class AcademicAdministrationIntentHandler(BaseIntentHandler):
    """
    Intent handler for Academic Administration intent.
    """

    def __init__(self):
        super().__init__()
        self._intent: Intent = Intent.ACADEMIC_ADMINISTRATION
        self.with_prompt_template(self._intent)
