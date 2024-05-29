from fastapi import FastAPI
from .dependencies.IntentClassifier import IntentClassifier
from .dependencies.DocumentEmbedder import DocumentEmbedder
from .dependencies.InformationRetriever import InformationRetriever
from .dependencies.ResponseGenerator import ResponseGenerator

class Application(FastAPI):

    def __init__(self, intent_classifier: IntentClassifier, info_retriever: InformationRetriever, response_generator: ResponseGenerator, document_embedder: DocumentEmbedder):
        super().__init__()
