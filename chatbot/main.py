from dotenv import load_dotenv
from chatbot.Application import Application
from chatbot.config import Configuration
from chatbot.dependencies.IntentClassifier import IntentClassifier
from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
from chatbot.dependencies.InformationRetriever import InformationRetriever
from chatbot.dependencies.ResponseGenerator import ResponseGenerator
from chatbot.logger import configure_logging, logger
from fastapi import FastAPI
from chatbot.routers import router
import os


def load_configuration_file(path: str = "configuration.yaml"):
    """
    Loads a configuration file and initializes a `Configuration` object.

    Args:
        path (str, optional): The path to the configuration file. Defaults to "configuration.yaml".

    Returns:
        None
    """
    Configuration(path=path)


def setup_server() -> FastAPI:
    """
    Sets up a FastAPI server instance with an initialized Application and included router.
    Returns:
        A FastAPI server instance.

    Raises:
        None
    """
    server = FastAPI()
    server.state.application = Application(
        intent_classifier=IntentClassifier(),
        document_embedder=DocumentEmbedder(),
        information_retriever=InformationRetriever(),
        response_generator=ResponseGenerator(),
    )
    server.include_router(router)

    return server


def run_app(server: FastAPI):
    """
    Runs the FastAPI application using uvicorn.

    :param server: A FastAPI server instance
    :type server: FastAPI

    :return: None
    :rtype: None
    """
    import uvicorn

    try:
        uvicorn.run(server, host="0.0.0.0", port=os.getenv("PORT", 8000))
    except KeyboardInterrupt:
        logger.info("Application terminated by user.")
        pass


def main():
    """
    Initializes the main function of the program.

    This function loads environment variables from a .env file, configures logging,
    loads the configuration from a specified YAML file, and runs the FastAPI application
    using uvicorn.

    Parameters:
        None

    Returns:
        None
    """
    configure_logging()  # Configure logging

    # Load the configuration from the specified YAML file.
    load_configuration_file("configuration.yaml")
    run_app(setup_server())

if __name__ == "__main__":
    main()
