import os
import speech_recognition as sr

def speech_to_text(audio_path):
    """
    Uses SpeechRecognition + Google Web Speech API (free).
    Converts to WAV if needed.
    """
    recognizer = sr.Recognizer()
    ext = os.path.splitext(audio_path)[1].lower()

    wav_path = audio_path
    if ext != ".wav":
        try:
            from pydub import AudioSegment
            wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
            AudioSegment.from_file(audio_path).export(wav_path, format="wav")
        except Exception as e:
            return f"[ERROR converting audio to WAV: {e}]"

    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"[ERROR transcribing audio: {e}]"
