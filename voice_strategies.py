import os
import platform
import subprocess
import tempfile

import pygame
from gtts import gTTS

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class VoiceStrategy:
    """Base strategy for converting text into speech."""

    def speak(self, text, lang):
        raise NotImplementedError


class CloudTTSStrategy(VoiceStrategy):
    """Uses Google Text-to-Speech through gTTS."""

    def speak(self, text, lang):
        tts = gTTS(text=text, lang=lang, slow=False)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as fp:
            audio_path = fp.name
            tts.save(audio_path)

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception:
            system = platform.system()

            if system == "Windows":
                os.system(
                    f'start /min wmplayer "{audio_path}"'
                )

            elif system == "Darwin":
                subprocess.run(["afplay", audio_path])

            else:
                os.system(
                    f"mpg123 '{audio_path}' 2>/dev/null"
                )

        finally:
            if os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except PermissionError:
                    pass


class OfflineTTSStrategy(VoiceStrategy):
    """Uses the local pyttsx3 speech engine."""

    def speak(self, text, lang):
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 is not installed.")

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


class OSVoiceStrategy(VoiceStrategy):
    """Uses the operating system's built-in speech capability."""

    def speak(self, text, lang):
        system = platform.system()

        if system == "Windows":
            escaped = text.replace('"', "'")

            cmd = (
                'PowerShell -Command '
                '"Add-Type -AssemblyName System.Speech; '
                '$speak = New-Object '
                'System.Speech.Synthesis.SpeechSynthesizer; '
                f'$speak.Speak(\\"{escaped}\\");"'
            )

            os.system(cmd)
            return

        if system == "Darwin":
            subprocess.run(["say", text])
            return

        subprocess.run(["espeak", text])


class VoiceContext:
    """Context that uses a selected voice strategy."""

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def speak(self, text, lang):
        return self.strategy.speak(text, lang)