from django import forms

from .models import Status, TranscribeAudio


class TranscribeAudioForm(forms.ModelForm):
    class Meta:
        model = TranscribeAudio
        fields = ("status", "audio_file")