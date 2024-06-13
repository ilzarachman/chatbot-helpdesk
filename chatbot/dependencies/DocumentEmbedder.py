from .IntentClassifier import Intent
from .ModelLoader import ModelLoader
from .contracts.TextEmbedder import TextEmbedder
from ..config import Configuration
from langchain_community import document_loaders


class DocumentEmbedder:
    """This class is responsible for embedding documents into vectors."""
    _supported_document_types = {
        "txt": document_loaders.TextLoader,
        "pdf": document_loaders.PDFLoader
    }

    def __init__(self):
        """Initialize the DocumentEmbedder class."""
        self._embedding_model = ModelLoader.load_model(
            Configuration.get("document_embedder.model")
        )

    def save_document_to_vectorstore(self, doc_path: str, doc_category: Intent) -> None:
        """
        Saves a document to the vectorstorage.

        Args:
            doc_path (str): The path to the document.
            doc_category (Intent): The type of the document.

        Returns:
            None

        Raises:
            RuntimeError: document can't be saved.
        """
        # 1. load the document
        raw_doc = self._load_document(doc_path)
        # 2. split the document into chunks
        # 3. embed the chunks
        # 4. save the document to the vectorstorage

    def _load_document(self, doc_path: str) -> str:
        """
        Loads a document from a file.

        Args:
            doc_path (str): The path to the document.

        Returns:
            str: The content of the document.

        Raises:
            RuntimeError: document can't be loaded.
        """
        doc_type = doc_path.split(".")[-1]
        if doc_type in self._supported_document_types:
            loader = self._supported_document_types[doc_type]
            return loader(doc_path).load()
        raise RuntimeError("document can't be loaded.")
