import os
import random
import string

from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from pydub import AudioSegment
from users.models import User


def generate_short_id():
    length = 8  # You can adjust the length as needed
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters.upper()) for i in range(length))


class TranscribeAudio(models.Model):
    """
    Model to store the audio file and its transcription
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        default=generate_short_id,
    )
    slug = models.SlugField(unique=True, blank=True)
    audio_file = models.FileField(upload_to="audio_files/")
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    probability = models.FloatField(null=True, blank=True)
    transcription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transcriptions",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.audio_file and not self.audio_file.name.endswith(".mp3"):
            # Load the audio file using pydub
            audio = AudioSegment.from_file(self.audio_file)
            # Convert the audio to MP3 format
            audio_data = audio.export(format="mp3")

            # Generate a new filename with an MP3 extension
            filename, _ = os.path.splitext(self.audio_file.name)
            mp3_filename = f"{filename}.mp3"

            # Save the converted MP3 file
            self.audio_file.save(
                mp3_filename, ContentFile(audio_data.read()), save=False
            )
            audio_data.close()

        super(TranscribeAudio, self).save(*args, **kwargs)

    def get_duration(self):
        if self.start and self.end:
            return self.end - self.start
        return ""

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.audio_file.name}"
        return f"{self.audio_file.name}"
