from celery import Celery
import whisper

app = Celery('tasks', broker='redis://localhost')

audio_file = ('audio.mp3')

@app.task
def transcribe(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, fp16=False)
    with open(f"{audio_file}.txt", "w") as f:
        f.write(result["text"])
    return result["text"][:4]


transcribe.delay(audio_file)