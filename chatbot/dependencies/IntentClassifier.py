import asyncio
from typing import Optional
from chatbot.config import Configuration
from chatbot.dependencies.ModelLoader import ModelLoader
from chatbot.dependencies.PromptManager import PromptManager
from chatbot.dependencies.contracts.TextGenerator import TextGenerator
from chatbot.dependencies.contracts.message import (
    Message,
    SystemMessage,
    UserMessage,
    AssistantMessage,
)
from chatbot.dependencies.utils.StringEnum import StringEnum


class Intent(StringEnum):
    ACADEMIC_ADMINISTRATION = "academic_administration_info"
    RESOURCE_SERVICE = "resource_service_info"
    SUPPORT = "need_assistant_support"
    OTHER = "other"

    @staticmethod
    def list() -> list[str]:
        """
        Helper method to load the intents from the intent classifier config.

        Returns:
            list[str]: A list of intents.
        """
        _intents = []
        for intent in Intent:
            _intents.append(intent.value)
        return _intents

    @staticmethod
    def get_intent(intent_value: str) -> "Intent":
        """
        Helper method to get the intent from the intent classifier config.

        Args:
            intent_value: The string representation of the intent.

        Returns:
            Intent: The corresponding Intent enum object.
        """
        return Intent.__members__.get(intent_value.upper(), Intent.OTHER)


class IntentDescription:
    """
    This class is used to get the description of an intent.
    """

    _describe: dict = {
        Intent.ACADEMIC_ADMINISTRATION: """Dukungan Akademik dan Administratif, meliputi,
        Pencarian Informasi (Information Inquiry): Ini mencakup pertanyaan tentang program akademik, detail mata kuliah, dosen, dan jadwal ujian. Contoh: 'Mata kuliah apa saja yang ditawarkan program studi Biologi semester ini?'.
        Prosedur Administratif (Administrative Procedures): Ini mencakup pertanyaan terkait proses administrasi universitas seperti pendaftaran, registrasi, bantuan keuangan, dan persyaratan kelulusan. Contoh: 'Bagaimana cara saya mengajukan beasiswa?'.
        Bantuan Akun Pribadi (Personal Account Assistance): Ini menangani masalah terkait akun mahasiswa, seperti masalah login, memperbarui informasi pribadi, dan mengakses catatan akademik. Contoh: 'Saya lupa password portal saya, bagaimana cara meresetnya?'.
        """,
        Intent.RESOURCE_SERVICE: """Sumber Daya dan Layanan Kampus, meliputi,
        Dukungan Teknis (Technical Support): Ini untuk masalah teknis dengan sumber daya IT kampus, seperti koneksi jaringan, instalasi perangkat lunak, dan masalah perangkat keras. Contoh: "Printer di perpustakaan tidak berfungsi, siapa yang bisa saya hubungi?".
        Lokasi Sumber Daya (Resource Locations): Ini termasuk permintaan petunjuk arah atau lokasi fasilitas kampus seperti ruang kuliah, kompleks olahraga, dan layanan makan. Contoh: "Di mana lokasi Pusat Layanan Mahasiswa?".
        Layanan Kampus (Campus Services): Ini mencakup layanan yang disediakan oleh universitas, seperti konseling, layanan kesehatan, bimbingan karir, dan klub ekstrakurikuler. Contoh: "Bisakah Anda memberi tahu saya jam kerja Pusat Karir?".
        """,
        Intent.SUPPORT: """Bantuan Mendesak, meliputi,
        Informasi Darurat (Emergency Information): Ini untuk bantuan segera selama keadaan darurat, seperti melaporkan kecelakaan, masalah keamanan, atau bantuan medis mendesak. Contoh: "Ada pemadaman listrik di asrama, apa yang harus saya lakukan?".
        Umpan Balik dan Keluhan (Feedback and Complaints): Ini menangkap umpan balik atau keluhan pengguna tentang any aspek kehidupan kampus, mulai dari kualitas makanan kafetaria hingga lingkungan kelas. Contoh: "Saya ingin melaporkan masalah dengan AC di ruangan 101.".
        """,
        Intent.OTHER: """Jika kamu tidak tahu intent apa yang cocok, kamu bisa memberikan 'other' sebagai jawaban.""",
    }

    @staticmethod
    def get_description_string() -> str:
        """
        Helper method to get the description of the intent.

        Returns:
            str: The description of the intent.
        """
        _description = ""
        for intent, description in IntentDescription._describe.items():
            _description += f"{intent.value}: {description}\n"
        return _description


class IntentClassifier:
    """
    This class is used to classify the intent of a message.
    """

    def __init__(self):
        """
        Initializes an instance of the IntentClassifier class.
        """
        self._intent_classifier_config: dict = Configuration.get("intent_classifier")
        self._model: TextGenerator = self._load_model()
        self._prompt_template: str = self._get_prompt_template()

    @staticmethod
    def _get_prompt_template() -> str:
        """
        Helper method to get the prompt template.

        Returns:
            str: The prompt template.
        """
        intents: str = ", ".join(Intent.list())
        return PromptManager.get_prompt(
            "intent_classification",
            "main_prompt",
            {
                "intent_list": intents,
                "intent_description": IntentDescription.get_description_string(),
            },
        )

    def _load_model(self) -> TextGenerator:
        """
        Helper method to load the Generator model.

        Returns:
            TextGenerator: The loaded model object.
        """
        _model_name: str = self._intent_classifier_config.get("model")
        return ModelLoader.load_model(_model_name)

    def _build_prompt_with_examples(self, message: str) -> list[Message]:
        """
        Helper method to build the prompt with example.

        Parameters:
            message (str): The message to be classified.

        Returns:
            list[Message]: The list of messages.
        """
        prompts: list[Message] = [
            SystemMessage(self._prompt_template),
            UserMessage(message),
        ]

        return prompts

    async def classify(self, message: str) -> Intent:
        """Classify the intent of the given message.

        This function takes a message as input and returns the intent of the message as a string.

        Parameters:
            message (str): The message to be classified.

        Returns:
            str: The intent of the message.
        """
        prompts: list[Message] = self._build_prompt_with_examples(message)

        intent_str = await self._model.generate_async(
            prompts, self._intent_classifier_config.get("model_settings")
        )

        try:
            loop = asyncio.get_running_loop()
            if loop:
                print(f"Active event loop: {loop}")
        except RuntimeError:  # Handles case where no loop is running
            print("No active event loop found")

        return Intent(intent_str)

    def _build_history_messages(
        self, message: str, history: list[dict]
    ) -> list[Message]:
        """
        Helper method to build the history messages.

        Parameters:
            message (str): The message to be classified.
            history (list[dict]): The history list.

        Returns:
            list[Message]: The list of messages.
        """
        prompts: list[Message] = [SystemMessage(self._prompt_template)]

        for msg in history:
            prompts.append(UserMessage(msg["A"]))
        prompts.append(UserMessage(message))

        return prompts

    async def classify_with_history(self, message: str, history: list[dict]) -> Intent:
        """Classify the intent of the given message with history.

        This function takes a message and a history as input and returns the intent of the message as a string.

        Parameters:
            message (str): The message to be classified.
            history (list[dict]): The history list.

        Returns:
            str: The intent of the message.
        """
        prompts: list[Message] = self._build_history_messages(message, history)

        intent_str = await self._model.generate_async(
            prompts, self._intent_classifier_config.get("model_settings")
        )

        return Intent(intent_str)
