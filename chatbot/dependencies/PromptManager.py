from typing import Optional

from chatbot.config import Configuration
from jinja2 import Template
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
    def get_prompt(cls, prompt_filename: str, prompt_name: str, context: Optional[dict] = None) -> str:
        """
        A method to get a prompt based on the prompt filename, prompt name, and optional context.

        Args:
            cls: The class reference.
            prompt_filename (str): The filename of the prompt.
            prompt_name (str): The name of the prompt.
            context (Optional[dict], optional): Additional context for rendering the prompt. Defaults to None.

        Returns:
            str: The rendered prompt.

        Raises:
            KeyError: If the prompt name is not found in the prompt file.
        """
        try:
            prompt_file = cls._read_prompt_file(prompt_filename)
            template_string = Template(prompt_file[prompt_name])

            if context:
                return template_string.render(**context)
            else:
                return template_string.render()

        except KeyError:
            raise KeyError(f"Prompt '{prompt_name}' not found in '{prompt_filename}' file.")
        except Exception as e:
            raise e

    @classmethod
    def get_prompt_template(cls, prompt_filename: str, prompt_name: str) -> Template:
        """
        A method to get a prompt template based on the prompt filename and prompt name.

        Args:
            cls: The class reference.
            prompt_filename (str): The filename of the prompt.
            prompt_name (str): The name of the prompt.

        Returns:
            Template: The prompt template.

        Raises:
            KeyError: If the prompt name is not found in the prompt file.
        """
        try:
            prompt_file = cls._read_prompt_file(prompt_filename)
            template_string = Template(prompt_file[prompt_name])
            return template_string
        except KeyError:
            raise KeyError(f"Prompt '{prompt_name}' not found in '{prompt_filename}' file.")
        except Exception as e:
            raise e

    @classmethod
    def give_context_to_template(cls, prompt_template: Template, context: dict) -> str:
        """
        A method to give context to a prompt template.

        Args:
            cls: The class reference.
            prompt_template (Template): The prompt template.
            context (dict): The context to give to the prompt template.

        Returns:
            Template: The prompt template with the context.

        Raises:
            ValueError: If the prompt template is not a Template object.
        """
        if not isinstance(prompt_template, Template):
            raise ValueError("Prompt template must be a Template object.")

        try:
            return prompt_template.render(**context)
        except Exception as e:
            raise e

