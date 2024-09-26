from typing import Optional

from .Application import Application

app: Optional[Application] = None


def set_application(application: Application):
    """
    Sets the application instance.

    This function supposed to be used for dependency injection in FastAPI applications.

    Args:
        application (Application): The application instance.

    Returns:
        None
    """
    global app
    app = application


def get_application() -> Application | None:
    """
    Returns the application instance.

    This function supposed to be used for dependency injection in FastAPI applications.

    Returns:
        Application: The application instance.
    """
    return app
