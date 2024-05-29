from ..contracts.TextGenerator import TextGenerator

class Gemini(TextGenerator):
    def generate(self, text):
        return text