# board/forms.py
from django import forms

class ChatForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 1, 
            'placeholder': '질문을 입력하세요...',
            'style': 'overflow:hidden;',
            # 'style': 'overflow:hidden; resize: vertical; width: 100%;'
        }),
        label=''
    )
