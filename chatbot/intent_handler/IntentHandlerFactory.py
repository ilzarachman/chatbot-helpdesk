from .AcademicAdministrationIntentHandler import AcademicAdministrationIntentHandler
from .OtherIntentHandler import OtherIntentHandler
from .ResourceServiceIntentHandler import ResourceServiceIntentHandler
from .SupportIntentHandler import SupportIntentHandler
from chatbot.dependencies.IntentClassifier import Intent
from chatbot.dependencies.contracts.BaseIntentHandler import BaseIntentHandler


class IntentHandlerFactory:
    handlers: dict[Intent, BaseIntentHandler] = {
        Intent.ACADEMIC_ADMINISTRATION: AcademicAdministrationIntentHandler(),
        Intent.RESOURCE_SERVICE: ResourceServiceIntentHandler(),
        Intent.SUPPORT: SupportIntentHandler(),
        Intent.OTHER: OtherIntentHandler(),
    }

    @staticmethod
    def get_handler(intent: Intent) -> BaseIntentHandler:
        """
        Get the intent handler for the given intent.

        Parameters:
            intent (Intent): The intent to get the handler for.

        Returns:
            BaseIntentHandler: The intent handler for the given intent.
        """
        return IntentHandlerFactory.handlers.get(intent)
