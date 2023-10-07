from celery import shared_task

from .models import TranscribeAudio, Status


@shared_task
def transcribe_audio(task_id):
    task = TranscribeAudio.objects.get(id=task_id)
    audio_file = task.audio_file
    result = task.transcribe(audio_file, fp16=False)
    task.transcription = result['text']
    task.status = Status.objects.get(status__icontains='transcribed')
    return f'{task.status}'

#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file, fp16=False)
#     with open(f"{audio_file}.txt", "w") as f:
#         f.write(result["text"])
#     return result["text"][:4]
