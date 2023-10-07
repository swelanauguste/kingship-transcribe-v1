from django.db import models


class Status(models.Model):
    """
    Model to store the status of the audio file
    """

    status = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.status


class TranscribeAudio(models.Model):
    """
    Model to store the audio file and its transcription
    """

    audio_file = models.FileField(upload_to="audio_files/")
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="status_list", null=True, default=1
    )
    transcription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.audio_file.name}"
