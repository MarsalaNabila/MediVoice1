import unittest
from unittest.mock import Mock, patch

import voice_alert


class ImmediateThread:
    def __init__(self, target, daemon):
        self.target = target
        self.daemon = daemon

    def start(self):
        self.target()


class VoiceAlertTests(unittest.TestCase):
    def test_speak_ignores_blank_text(self):
        with patch("voice_alert.threading.Thread") as thread:
            self.assertIsNone(voice_alert.speak("   "))
        thread.assert_not_called()

    def test_speak_normalizes_bangla_language_alias(self):
        with patch("voice_alert.threading.Thread", ImmediateThread), patch(
            "voice_alert._speak_with_cloud_tts"
        ) as cloud:
            voice_alert.speak("Take medicine", "Bangla")
        cloud.assert_called_once_with("Take medicine", "bn")

    def test_speak_uses_english_for_unknown_language(self):
        with patch("voice_alert.threading.Thread", ImmediateThread), patch(
            "voice_alert._speak_with_cloud_tts"
        ) as cloud:
            voice_alert.speak("Take medicine", "unknown")
        cloud.assert_called_once_with("Take medicine", "en")

    def test_speak_uses_offline_fallback_after_cloud_failure(self):
        with patch("voice_alert.threading.Thread", ImmediateThread), patch(
            "voice_alert._speak_with_cloud_tts", side_effect=RuntimeError("offline")
        ), patch("voice_alert._speak_offline", return_value=True) as offline:
            voice_alert.speak("Take medicine", "en")
        offline.assert_called_once_with("Take medicine")

    def test_stop_voice_terminates_active_process(self):
        process = Mock()
        process.terminate = Mock()
        process.kill = Mock()
        voice_alert._ACTIVE_VOICE_PROCESS = process

        with patch("voice_alert.pygame.mixer.get_init", return_value=False):
            voice_alert.stop_voice()

        process.terminate.assert_called_once()
        process.kill.assert_called_once()
        self.assertIsNone(voice_alert._ACTIVE_VOICE_PROCESS)


if __name__ == "__main__":
    unittest.main()
