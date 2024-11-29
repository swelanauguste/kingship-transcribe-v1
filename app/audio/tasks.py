from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
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
        try:
            for segment in segments:
                text += segment.text
                task.transcription = text
                task.save()
        except Exception as e:
            messages.error(e)
            send_mail(
                "Transcription Failed",
                "Your transcription failed, please try again",
                settings.DEFAULT_FROM_EMAIL,
                [task.created_by.email],
                fail_silently=False,
            )
        task.transcription = text
        task.end = timezone.now()
        task.save()
        send_mail(
            "Transcription Complete",
            "Your transcription is ready",
            settings.DEFAULT_FROM_EMAIL,
            [task.created_by.email],
            fail_silently=False,
        )

        with open(f"transcription/{task.name}.txt", "w") as f:
            f.write(text)
        return f"Transcription successful"
    except Exception as e:
        send_mail(
            "Transcription Failed",
            "Your transcription failed, please try again",
            settings.DEFAULT_FROM_EMAIL,
            [task.created_by.email],
            fail_silently=False,
        )
        return f"Transcription failed error {e}"
