import pathlib


def project_path(*args) -> pathlib.Path:
    """
    Get the project path.

    Parameters:
        *args: The arguments to join to the project path.

    Returns:
        pathlib.Path: The project path.
    """
    path = pathlib.Path(__file__).parent.parent.parent.parent
    if args:
        return path.joinpath(*args)
    else:
        return path
