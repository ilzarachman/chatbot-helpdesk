from chatbot.Application import Application

app = Application()

@app.get("/")
async def root():
    return {"message": "Connected!"}

def main():
    """
    Runs the FastAPI application using uvicorn.

    This function imports the uvicorn module and calls its `run` function to start the FastAPI application. It specifies the application module as "main" and the application object as "app". The application is hosted on all available network interfaces (0.0.0.0) and listens on port 8000. The `reload` parameter is set to True, which enables automatic reloading of the application when changes are detected.

    This function is typically used as the entry point for running the FastAPI application.

    Parameters:
        None

    Returns:
        None
    """
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()