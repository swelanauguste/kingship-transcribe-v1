from django.urls import path

from .views import (
    TranscribeAudioDetailView,
    TranscribeAudioListView,
    create_transcription,
    export_to_word,
)

urlpatterns = [
    path("", TranscribeAudioListView.as_view(), name="list"),
    path("transcribe/", create_transcription, name="transcribe"),
    path("detail/<slug:slug>/", TranscribeAudioDetailView.as_view(), name="detail"),
    path("export_to_word/<slug:slug>/", export_to_word, name="export_to_word"),
]
