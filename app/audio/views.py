import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from docx import Document

from .forms import TranscribeAudioForm
from .models import TranscribeAudio
from .tasks import transcribe_audio


def create_transcription(request):
    if request.method == "POST":
        form = TranscribeAudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            transcribe_audio_thread = threading.Thread(
                target=transcribe_audio, args=(form.instance.id,)
            )
            transcribe_audio_thread.start()
        return redirect("detail", pk=form.instance.id)

    else:
        form = TranscribeAudioForm()
    return render(request, "audio/transcribe_audio.html", {"form": form})


class TranscribeAudioListView(ListView):
    model = TranscribeAudio


class TranscribeAudioDetailView(DetailView):
    model = TranscribeAudio


def export_to_word(request, pk):
    # Create a new Document
    doc = Document()

    # Add a title
    doc.add_heading("Data Export", 0)

    # Get the data you want to export
    data = TranscribeAudio.objects.get(pk=pk)

    # Add data to the document
    doc.add_paragraph(f"Name: {data.name}")
    doc.add_paragraph(f"Probability: {data.probability}")
    doc.add_paragraph(f"Duration: {data.get_duration()}")
    doc.add_paragraph(f"Description: {data.transcription}")
    doc.add_paragraph("")  # Blank line between entries

    # Prepare the response to download the Word document
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = 'attachment; filename=f"export.docx"'

    # Save the document to the response
    doc.save(response)
    return response
