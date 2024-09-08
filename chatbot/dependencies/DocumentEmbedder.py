import importlib

from langchain_community import document_loaders
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

from .IntentClassifier import Intent
from .ModelLoader import ModelLoader
from .contracts.TextEmbedder import TextEmbedder
from .utils.path_utils import project_path
from ..config import Configuration


class DocumentEmbedder:
    """This class is responsible for embedding documents into vectors."""

    supported_document_types: dict[str, type(BaseLoader)] = {
        "txt": document_loaders.TextLoader,
        "pdf": document_loaders.PyPDFLoader,
        "docx": document_loaders.Docx2txtLoader,
        "doc": document_loaders.Docx2txtLoader,
        "csv": document_loaders.CSVLoader,
    }
    """
    Supported document types.

    Supported document types are:
    - txt
    - pdf
    - docx
    """

    _instance = None

    def __init__(self):
        """Initialize the DocumentEmbedder class."""
        self._embedding_model: TextEmbedder = ModelLoader.load_model(
            Configuration.get("document_embedder.embedding_model")
        )
        self._text_splitter_config = Configuration.get(
            "document_embedder.text_splitter"
        )
        self._text_splitter: TextSplitter = self._get_text_splitter()

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

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
        try:
            raw_doc = self._load_document(doc_path)
            documents = self._split_raw_document(raw_doc)
            self._save_to_faiss_index(documents, doc_category)
        except Exception as e:
            raise RuntimeError(f"Error saving document to vectorstore: {e}")

    def save_public_document_to_vectorstore(
        self, doc_path: str, doc_category: Intent
    ) -> None:
        """
        Saves a public document to the vectorstorage.

        Args:
            doc_path (str): The path to the document.
            doc_category (Intent): The type of the document.

        Returns:
            None

        Raises:
            RuntimeError: document can't be saved.
        """
        try:
            raw_doc = self._load_document(doc_path)
            documents = self._split_raw_document(raw_doc)
            self._save_public_to_faiss_index(documents, doc_category)
        except Exception as e:
            raise RuntimeError(f"Error saving document to vectorstore: {e}")

    def _load_document(self, doc_path: str) -> list[Document]:
        """
        Loads a document from a file.

        Args:
            doc_path (str): The path to the document.

        Returns:
            str: The content of the document.

        Raises:
            RuntimeError: If the document type is not supported.
        """
        doc_type = doc_path.split(".")[-1]
        if doc_type in self.supported_document_types:
            loader = self.supported_document_types[doc_type]
            try:
                _loader = loader(doc_path)
                return _loader.load()
            except Exception as e:
                raise RuntimeError(f"Error loading document: {e}")
        else:
            raise RuntimeError("Document type not supported.")

    def _get_text_splitter(self) -> TextSplitter:
        """
        Dynamically loads the text splitter based on the configuration.

        Returns:
            TextSplitter: The text splitter.
        """
        text_splitter_type = self._text_splitter_config.get("type")
        module = importlib.import_module(f"langchain_text_splitters")
        params = self._text_splitter_config.get("params")
        text_splitter = getattr(module, text_splitter_type)(**params)
        return text_splitter

    def _split_raw_document(self, raw_doc: list[Document]) -> list[Document]:
        """
        Splits a raw document into chunks.

        Args:
            raw_doc (list[Document]): The raw document.

        Returns:
            list[Document]: The split document.
        """
        return self._text_splitter.split_documents(raw_doc)

    def _save_to_faiss_index(self, documents: list[Document], category: Intent) -> None:
        """
        Saves a document to the FAISS index.

        Args:
            documents (list[Document]): The document to be saved.

        Returns:
            None
        """
        faiss_root_dir = project_path("faiss")
        faiss_category_dir = faiss_root_dir / category.value

        if not faiss_category_dir.exists():
            self._embedding_model.save_to_faiss_index(documents, faiss_category_dir)
            return

        self._embedding_model.add_data_to_faiss_index(documents, faiss_category_dir)

    def _save_public_to_faiss_index(
        self, documents: list[Document], category: Intent
    ) -> None:
        """
        Saves a public document to the FAISS index.

        Args:
            documents (list[Document]): The document to be saved.

        Returns:
            None
        """
        faiss_root_dir = project_path("faiss")
        faiss_category_dir = faiss_root_dir / (category.value + "_public")

        if not faiss_category_dir.exists():
            self._embedding_model.save_to_faiss_index(documents, faiss_category_dir)
            return

        self._embedding_model.add_data_to_faiss_index(documents, faiss_category_dir)

    def save_question_answer_to_vectorstore(
        self, question: str, answer: str, category: Intent
    ) -> None:
        """
        Saves a question.py and answer to the vectorstorage.

        Args:
            question (str): The question.py to be saved.
            answer (str): The answer to be saved.
            category (Intent): The type of the question.py and answer.

        Returns:
            None

        Raises:
            RuntimeError: question.py and answer can't be saved.
        """
        try:
            data = str({"question.py": question, "answer": answer})
            documents = self._split_raw_document([Document(data)])
            self._save_to_faiss_index(documents, category)
        except Exception as e:
            raise RuntimeError(
                f"Error saving question.py and answer to vectorstore: {e}"
            )

    def save_public_question_answer_to_vectorstore(
        self, question: str, answer: str, category: Intent
    ) -> None:
        """
        Saves a public question.py and answer to the vectorstorage.

        Args:
            question (str): The question.py to be saved.
            answer (str): The answer to be saved.
            category (Intent): The type of the question.py and answer.

        Returns:
            None

        Raises:
            RuntimeError: question.py and answer can't be saved.
        """
        try:
            data = str({"question.py": question, "answer": answer})
            documents = self._split_raw_document([Document(data)])
            self._save_public_to_faiss_index(documents, category)
        except Exception as e:
            raise RuntimeError(
                f"Error saving question.py and answer to vectorstore: {e}"
            )
