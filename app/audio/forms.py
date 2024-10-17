from django import forms

from .models import TranscribeAudio


class TranscribeAudioForm(forms.ModelForm):
    class Meta:
        model = TranscribeAudio
        fields = (
            "name",
            "audio_file",
        )
