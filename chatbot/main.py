from dotenv import load_dotenv
from chatbot.Application import Application
from chatbot.logger import configure_logging
from fastapi import FastAPI
from chatbot.routers import router

load_dotenv(override=True)
configure_logging()

server = FastAPI()
app = Application()

server.include_router(router)

def main():
    """
    Runs the FastAPI application using uvicorn.

    This function is typically used as the entry point for running the FastAPI application.

    Parameters:
        None

    Returns:
        None
    """
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()