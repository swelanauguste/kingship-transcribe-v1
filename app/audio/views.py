from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import TranscribeAudioForm
from .models import TranscribeAudio
from .tasks import transcribe_audio


def create_transcription(request):
    if request.method == 'POST':
        form = TranscribeAudioForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['audio_file']
            form.save()
            transcribe_audio.delay(form.instance.id)
            return redirect('/')
    else:
        form = TranscribeAudioForm()
    return render(request, 'audio/transcribe_audio.html', {'form': form})

class TranscribeAudioListView(ListView):
    model = TranscribeAudio


class TranscribeAudioDetailView(DetailView):
    model = TranscribeAudio
