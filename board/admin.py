# board/admin.py
from django.contrib import admin
from .models import ChatMessage, Conversation, UploadedFile

admin.site.register(ChatMessage)
admin.site.register(Conversation)
admin.site.register(UploadedFile)
