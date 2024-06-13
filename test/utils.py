import os
import unittest

import pytest

from chatbot.dependencies.utils.path_utils import project_path


class TestUtils(unittest.TestCase):
    @pytest.mark.skip
    def test_project_path(self):
        self.assertEqual(str(project_path("test")), os.path.join(os.getcwd(), "test"))