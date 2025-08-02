from abc import ABC, abstractmethod
import logging
import asyncio
import edge_tts

logging.basicConfig(level=logging.INFO)

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
        logging.info("Initializing pyttsx3 engine.")
        self.engine = pyttsx3.init()
        logging.info("pyttsx3 engine initialized.")

    def synthesize(self, text: str, output_file: str, voice: str):
        try:
            logging.info(f"Synthesizing audio with voice: {voice}")
            if voice:
                self.engine.setProperty('voice', voice)
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
            logging.info("Audio synthesis complete.")
        except Exception as e:
            logging.error(f"Error synthesizing audio: {e}")
            raise ValueError(f"Error synthesizing audio: {e}")

    def get_voices(self) -> list[str]:
        try:
            logging.info("Getting available voices.")
            voices = self.engine.getProperty('voices')
            voice_ids = [v.id for v in voices]
            logging.info(f"Found voices: {voice_ids}")
            return voice_ids
        except Exception as e:
            logging.error(f"Error getting voices: {e}")
            return []

class EdgeTtsEngine(TTSEngine):
    """
    TTS engine using edge-tts.
    """
    def __init__(self):
        logging.info("Initializing edge-tts engine.")

    def synthesize(self, text: str, output_file: str, voice: str):
        try:
            logging.info(f"Synthesizing audio with voice: {voice}")
            asyncio.run(self._synthesize_async(text, output_file, voice))
            logging.info("Audio synthesis complete.")
        except Exception as e:
            logging.error(f"Error synthesizing audio: {e}")
            raise ValueError(f"Error synthesizing audio: {e}")

    async def _synthesize_async(self, text: str, output_file: str, voice: str):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    def get_voices(self) -> list[str]:
        try:
            logging.info("Getting available voices.")
            voices = asyncio.run(self._get_voices_async())
            voice_names = [v['ShortName'] for v in voices]
            logging.info(f"Found voices: {voice_names}")
            return voice_names
        except Exception as e:
            logging.error(f"Error getting voices: {e}")
            return []

    async def _get_voices_async(self):
        return await edge_tts.list_voices()