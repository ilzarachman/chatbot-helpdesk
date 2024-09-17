from dotenv import load_dotenv

import os
from chatbot.logger import configure_logging, logger
from fastapi import FastAPI

load_dotenv(override=True)


def setup_server() -> FastAPI:
    """
    Sets up a FastAPI server instance with an initialized Application and included router.
    Returns:
        A FastAPI server instance.

    Raises:
        None
    """
    from chatbot.routers import router
    from chatbot.app import set_application
    from chatbot.Application import Application
    from chatbot.dependencies.DocumentEmbedder import DocumentEmbedder
    from chatbot.dependencies.InformationRetriever import InformationRetriever
    from chatbot.dependencies.IntentClassifier import IntentClassifier
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.sessions import SessionMiddleware

    configure_logging()  # Configure logging

    set_application(
        Application(
            intent_classifier=IntentClassifier(),
            document_embedder=DocumentEmbedder(),
            information_retriever=InformationRetriever(),
        )
    )
    server = FastAPI()

    origins = ["http://localhost:3000", "http://localhost:3001"]

    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    SESSION_SECRET_KEY = "2ddwqws2no"

    server.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

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


def check_environment_variables():
    """
    Checks if all required environment variables are set.

    :return: None
    :rtype: None
    """
    required_vars = []

    # load file .example-env
    with open(".example-env", "r") as f:
        for line in f:
            if line.startswith("#") or line.isspace():
                continue
            var, value = line.strip().split("=")
            required_vars.append(var)

    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Environment variable {var} is not set.")


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
    check_environment_variables()
    run_app(setup_server())


if __name__ == "__main__":
    main()
