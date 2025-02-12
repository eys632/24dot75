from django.urls import path
from .views import chat_view, stream_answer, upload_file, conversation_list_admin, file_upload_list_admin

app_name = "board"

urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("chat/<int:conversation_id>/", chat_view, name="chat_detail"),
    path("stream_answer/", stream_answer, name="stream_answer"),
    path("upload_file/", upload_file, name="upload_file"),
    path("admin/conversations/", conversation_list_admin, name="admin_conversations"),
    path("admin/files/", file_upload_list_admin, name="admin_files"),
]
