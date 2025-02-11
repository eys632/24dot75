from .models import Board

def board_list_context(request):
    return {'board_list': Board.objects.all()}  # 모든 게시글을 템플릿에서 사용 가능하도록 전달
