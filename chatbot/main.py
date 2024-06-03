from dotenv import load_dotenv
from chatbot.Application import Application
from chatbot.config import Configuration
from chatbot.logger import configure_logging
from fastapi import FastAPI
from chatbot.routers import router

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

    :return: A FastAPI server instance.
    :rtype: FastAPI
    """
    server = FastAPI()
    server.state.application = Application()
    server.include_router(router)
    return server

def main(server: FastAPI):
    """
    Runs the FastAPI application using uvicorn.

    :param server: A FastAPI server instance
    :type server: FastAPI

    :return: None
    :rtype: None
    """
    import uvicorn

    uvicorn.run(server, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    load_dotenv(override=True) # Load environment variables from .env file
    configure_logging() # Configure logging
    
    # Load the configuration from the specified YAML file.
    load_configuration_file("configuration.yaml")
    main(setup_server())
