from enum import Enum


class StringEnum(Enum):
    def __new__(cls, value):
        """
        Creates and returns a new instance of the class with the specified value.

        Args:
            cls: The class itself.
            value: The value to assign to the new instance.

        Returns:
            The newly created instance with the assigned value.
        """
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __str__(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        return str(self.value)
