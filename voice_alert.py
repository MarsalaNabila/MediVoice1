from voice_strategies import (
    CloudTTSStrategy,
    OfflineTTSStrategy,
    OSVoiceStrategy,
    VoiceContext
)


def _get_language(lang_code):
    lang_map = {
        "english": "en",
        "en": "en",
        "bengali": "bn",
        "bangla": "bn",
        "bn": "bn"
    }

    return lang_map.get(
        (lang_code or "en").lower(),
        "en"
    )


def speak(text, lang_code="en"):
    """
    Convert text to speech.

    Strategy Pattern:
    The same speech request can use different
    voice strategies without changing the caller.
    """

    lang = _get_language(lang_code)

    strategies = [
        CloudTTSStrategy(),
        OfflineTTSStrategy(),
        OSVoiceStrategy()
    ]

    context = VoiceContext(strategies[0])

    for strategy in strategies:
        try:
            context.set_strategy(strategy)
            context.speak(text, lang)
            return

        except Exception as e:
            print(
                f"[Voice] {strategy.__class__.__name__} "
                f"failed ({e}). Trying next strategy..."
            )

    print(
        "[Voice] Unable to play voice alert "
        "with any strategy."
    )


def stop_voice():
    """
    Stop any currently playing voice alert.
    """

    try:
        import pygame

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    except Exception:
        pass