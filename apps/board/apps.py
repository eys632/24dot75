from django.apps import AppConfig

class BoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.board"

    def ready(self):
        # signals 모듈을 임포트하여 등록합니다.
        import apps.board.signals