from django.contrib import admin

from .models import TranscribeAudio, Status

admin.site.register(TranscribeAudio)
admin.site.register(Status)