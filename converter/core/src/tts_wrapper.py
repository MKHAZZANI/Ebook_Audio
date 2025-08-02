from abc import ABC, abstractmethod

class TTSEngine(ABC):
    """
    Abstract base class for Text-to-Speech engines.
    """
    @abstractmethod
    def synthesize(self, text: str, output_file: str, voice: str):
        pass

    @abstractmethod
    def get_voices(self) -> list[str]:
        pass

class Pyttsx3Engine(TTSEngine):
    """
    TTS engine using pyttsx3.
    """
    def __init__(self):
        import pyttsx3
        self.engine = pyttsx3.init()

    def synthesize(self, text: str, output_file: str, voice: str):
        try:
            if voice:
                self.engine.setProperty('voice', voice)
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
        except Exception as e:
            raise ValueError(f"Error synthesizing audio: {e}")

    def get_voices(self) -> list[str]:
        try:
            return [v.id for v in self.engine.getProperty('voices')]
        except Exception:
            return []