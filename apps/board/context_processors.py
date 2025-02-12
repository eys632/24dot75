from .models import Board  # 만약 Board 모델이 존재한다면

def board_list_context(request):
    return {"board_list": Board.objects.all()}  # 모든 게시글을 템플릿에서 사용 가능하도록 전달
