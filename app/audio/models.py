import random
import string

from django.db import models
from django.utils.text import slugify


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

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TranscribeAudio, self).save(*args, **kwargs)

    def get_duration(self):
        if self.start and self.end:
            return self.end - self.start
        return ""
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return f"{self.audio_file.name}"
