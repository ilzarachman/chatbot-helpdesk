import os

import fire
from infisical_client import InfisicalClient


class ChatbotApplication:
    def __init__(self):
        pass

    def start(self):
        from chatbot.main import main
        import subprocess

        main()
        return 0


def cli():
    fire.Fire(ChatbotApplication)
