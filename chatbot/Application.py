from typing import Optional, Union
import importlib
from .dependencies.IntentClassifier import IntentClassifier
from .dependencies.DocumentEmbedder import DocumentEmbedder
from .dependencies.InformationRetriever import InformationRetriever
from .dependencies.ResponseGenerator import ResponseGenerator
from .logger import logger


class Application:
    """
    This class represents the main application that integrates all the components of the chatbot.
    It provides a single point of access to the chatbot's functionality.
    """

    _instance: Optional["Application"] = None

    def __init__(
        self,
        intent_classifier: IntentClassifier,
        document_embedder: DocumentEmbedder,
        information_retriever: InformationRetriever,
    ):
        """
        Initialize the application.
        """
        self.intent_classifier = intent_classifier
        self.document_embedder = document_embedder
        self.information_retriever = information_retriever

        logger.info("Application initialized successfully!")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
