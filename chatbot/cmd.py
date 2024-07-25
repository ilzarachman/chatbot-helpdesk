import os

import fire
from infisical_client import InfisicalClient

from chatbot.dependencies.utils.path_utils import project_path


class ChatbotApplication:
    def __init__(self):
        pass

    def start(self):
        from chatbot.main import main
        import subprocess

        main()
        return 0

    def test(self):
        import pytest

        pytest.main([str(project_path("test")), "-m", "not integration"])
        return 0

    def _connect_alembic_to_db(self):
        from alembic.config import Config
        from alembic import command
        from chatbot.database import engine

        alembic_cfg = Config("alembic.ini")
        alembic_cfg.attributes["connection"] = engine.connect()

        return alembic_cfg

    def migration(self):
        from alembic import command

        alembic_cfg = self._connect_alembic_to_db()

        command.upgrade(alembic_cfg, "head")
        return 0

def cli():
    fire.Fire(ChatbotApplication)
