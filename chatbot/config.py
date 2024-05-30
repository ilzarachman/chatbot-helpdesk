import yaml

from .logger import logger

class Configuration:
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs) -> "Configuration":
        """
        Initializes a new instance of the Configuration class.

        Args:
            *args: The positional arguments to be passed to the __init__ method.
            **kwargs: The keyword arguments to be passed to the __init__ method.

        Returns:
            Configuration: An instance of the Configuration class.
        """
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, path: str):
        """
        Initializes a new instance of the Configuration class.

        Args:
            path (str): The path to the YAML file containing the configuration data.

        Returns:
            None

        Raises:
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        self.data = None
        with open(path, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
                logger.info("Configuration loaded successfully!")    
            except yaml.YAMLError as exc:
                print(exc)
                
    def get(self, key: str) -> any:
        """
        Get the value associated with the given key from the configuration data.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            any: The value associated with the given key. If the key is not found, a KeyError is raised.
        """
        try:
            return self.data[key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found in configuration data.")