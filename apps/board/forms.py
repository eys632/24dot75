from django import forms

class ChatForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 1,
            "placeholder": "질문을 입력하세요...",
            "style": "overflow:hidden;",
        }),
        label="",
    )
