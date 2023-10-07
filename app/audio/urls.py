from django.urls import path

from .views import TranscribeAudioDetailView, TranscribeAudioListView, create_transcription

urlpatterns = [
    path("", TranscribeAudioListView.as_view(), name="list"),
    path("transcribe/", create_transcription, name="transcribe"),
    path("detail/<int:pk>/", TranscribeAudioDetailView.as_view(), name="detail"),
]
