from __future__ import annotations


class VoiceService:
    def __init__(self):
        self.recognizer = None
        self.tts = None
        self.error = None
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.sr = sr
        except Exception as exc:
            self.error = str(exc)

        try:
            import pyttsx3
            self.tts = pyttsx3.init()
        except Exception as exc:
            self.error = str(exc)

    @property
    def available(self) -> bool:
        return self.recognizer is not None or self.tts is not None

    def speak(self, text: str) -> None:
        if self.tts is None:
            raise RuntimeError("TTS is unavailable. Install pyttsx3 and a platform voice backend.")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 12) -> str:
        if self.recognizer is None:
            raise RuntimeError("STT is unavailable. Install SpeechRecognition and a microphone backend.")
        with self.sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            return self.recognizer.recognize_google(audio)
        except Exception as exc:
            raise RuntimeError(f"Speech recognition failed: {exc}") from exc
