import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
with open("trans.txt", "w") as f:
    f.write(result["text"])
# result["text"]
