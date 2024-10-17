from django.db import models


class TranscribeAudio(models.Model):
    """
    Model to store the audio file and its transcription
    """

    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    audio_file = models.FileField(upload_to="audio_files/")
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    probability = models.FloatField(null=True, blank=True)
    transcription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-updated_at",
        ]

    def get_duration(self):
        if self.start and self.end:
            return self.end - self.start
        return ""

    def __str__(self):
        return f"{self.audio_file.name}"
