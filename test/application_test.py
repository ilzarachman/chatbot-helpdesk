import unittest
from chatbot.Application import Application

class TestApplication(unittest.TestCase):
    def test_get_instance_returns_the_same_instance(self):
        instance1 = Application()
        instance2 = Application.get_instance()
        self.assertEqual(instance1, instance2)