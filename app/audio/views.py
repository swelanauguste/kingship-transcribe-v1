from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import TranscribeAudioForm
from .models import TranscribeAudio
from .tasks import transcribe_audio


def create_transcription(request):
    if request.method == 'POST':
        form = TranscribeAudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            transcribe_audio.delay(form.instance.id)
            return render(request, 'audio/transcribe_audio_success.html')
    else:
        form = TranscribeAudioForm()
    return render(request, 'audio/transcribe_audio.html', {'form': form})

class TranscribeAudioListView(ListView):
    model = TranscribeAudio


class TranscribeAudioDetailView(DetailView):
    model = TranscribeAudio
