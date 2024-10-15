import whisper
from celery import shared_task

from .models import TranscribeAudio


@shared_task
def transcribe_audio(task_id):
    try:
        task = TranscribeAudio.objects.get(id=task_id)
        model = whisper.load_model("turbo")
        audio_file = task.audio_file.path
        result = model.transcribe(audio_file)
        task.transcription = result["text"]
        # task.status = Status.objects.get(status__icontains="transcribed")
        task.save()
        return f"Transcription successful for task {task.id}"
    except Exception as e:
        return f"Transcription failed for task {task.id} with error {e}"


#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file, fp16=False)
#     with open(f"{audio_file}.txt", "w") as f:
#         f.write(result["text"])
#     return result["text"][:4]
