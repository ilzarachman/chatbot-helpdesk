from typing import Optional

from chatbot.config import Configuration
import yaml


class PromptManager:
    _prompts_dir: Optional[str] = None

    @classmethod
    def _read_prompt_file(cls, prompt_name: str) -> dict:
        """
        A method to read a prompt file based on the prompt name.

        Args:
            cls: The class reference.
            prompt_name (str): The name of the prompt file to read.

        Returns:
            dict: The contents of the prompt file as a dictionary.

        Raises:
            FileNotFoundError: If the prompt file with the given name is not found.
        """
        if cls._prompts_dir is None:
            cls._prompts_dir = Configuration.get("prompts").get("directory")

        try:
            with open(f"{cls._prompts_dir}/{prompt_name}.yaml", "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt '{prompt_name}' not found.")

    @classmethod
    def get_prompt(cls, prompt_filename: str, prompt_name: str) -> str:
        """
        Get a prompt message from a prompt file.

        Args:
            cls: The class reference.
            prompt_filename (str): The name of the prompt file.
            prompt_name (str): The specific prompt to retrieve.

        Returns:
            str: The retrieved prompt message.

        Raises:
            KeyError: If the prompt with the given name is not found in the file.
        """
        prompt_file = cls._read_prompt_file(prompt_filename)
        try:
            return prompt_file[prompt_name]
        except KeyError:
            raise KeyError(f"Prompt '{prompt_name}' not found in '{prompt_filename}' file.")