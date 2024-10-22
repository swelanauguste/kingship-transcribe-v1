from django.urls import path

from . import views

urlpatterns = [
    path("", views.transcription_list_view, name="list"),
    path("transcribe/", views.create_transcription, name="transcribe"),
    path("detail/<slug:slug>/", views.transcription_detail_view, name="detail"),
    # path("detail/<slug:slug>/", TranscribeAudioDetailView.as_view(), name="detail"),
    path("export_to_word/<slug:slug>/", views.export_to_word, name="export_to_word"),
]
