from fastapi import FastAPI
from .dependencies.IntentClassifier import IntentClassifier
from .dependencies.DocumentEmbedder import DocumentEmbedder
from .dependencies.InformationRetriever import InformationRetriever
from .dependencies.ResponseGenerator import ResponseGenerator

class Application(FastAPI):

    def __init__(self):
        super().__init__()
