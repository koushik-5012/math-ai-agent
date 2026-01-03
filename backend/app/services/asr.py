import whisper

model = whisper.load_model("base")

def speech_to_text(audio_path: str) -> str:
    return model.transcribe(audio_path)["text"]
