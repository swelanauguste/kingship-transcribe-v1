from datetime import datetime

from django.contrib import messages
from django.utils import timezone
from faster_whisper import WhisperModel

from .models import TranscribeAudio


def transcribe_audio(task_id):
    try:
        task = TranscribeAudio.objects.get(id=task_id)
        model_size = "small"
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        audio_file = task.audio_file.path
        segments, info = model.transcribe(audio_file, beam_size=5)
        task.start = timezone.now()
        task.save()
        task.probability = info.language_probability
        task.save()
        text = ""
        for segment in segments:
            text += segment.text
            task.transcription = text
            task.save()
        task.transcription = text
        task.end = timezone.now()
        task.save()
        with open(f"transcription/{task.name}.txt", "w") as f:
            f.write(text)
        return f"Transcription successful"
    except Exception as e:
        return f"Transcription failed error {e}"
