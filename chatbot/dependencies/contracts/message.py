from abc import abstractmethod, ABC

class Message(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        pass

class AssistantMessage(Message):
    def __init__(self, message: str):
        """
        Initializes a new instance of the class.

        Args:
            message (str): The message to be stored in the instance.
        """
        self.message = message
    
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        pass

class UserMessage(Message):
    def __init__(self, message: str):
        """
        Initializes a new instance of the class.

        Args:
            message (str): The message to be stored in the instance.
        """
        self.message = message
    
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        pass