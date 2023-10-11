from django import forms

from .models import Status, TranscribeAudio


class TranscribeAudioForm(forms.ModelForm):
    class Meta:
        model = TranscribeAudio
        fields = (
            "name",
            "audio_file",
        )
        # widgets = {"audio_file": forms.FileInput(attrs={"class": "form-control"})}
