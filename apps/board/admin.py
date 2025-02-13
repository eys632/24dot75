from django.contrib import admin
from .models import ChatMessage, Conversation, UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    # file 필드 대신 file_name 메서드를 리스트에 표시하고, 클릭 시 변경폼으로 이동하도록 지정합니다.
    list_display = ('file_name', 'uploaded_at', 'is_processed')
    list_display_links = ('file_name',)  # file_name이 클릭 가능하도록 함

    def file_name(self, obj):
        # 파일명을 단순 텍스트로 반환 (하이퍼링크가 없음)
        return obj.file.name
    file_name.short_description = "파일 이름"

admin.site.register(ChatMessage)
admin.site.register(Conversation)
admin.site.register(UploadedFile, UploadedFileAdmin)
