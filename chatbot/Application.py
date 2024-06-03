from typing import Optional
from .dependencies.IntentClassifier import IntentClassifier
from .dependencies.DocumentEmbedder import DocumentEmbedder
from .dependencies.InformationRetriever import InformationRetriever
from .dependencies.ResponseGenerator import ResponseGenerator
from .logger import logger

class Application:
    _instance: Optional["Application"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the application.
        """
        self.intent_classifier = IntentClassifier()
        self.document_embedder = DocumentEmbedder()
        self.information_retriever = InformationRetriever()
        self.response_generator = ResponseGenerator()
        
        logger.info("Application initialized successfully!")

    @classmethod
    def get_instance(cls) -> "Application":
        """
        Get the instance of the application.

        Returns:
            Application: The instance of the application.
        """
        if not cls._instance:
            cls._instance = Application()
        return cls._instance
