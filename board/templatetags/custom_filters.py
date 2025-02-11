from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def media_url(path):
    """미디어 URL을 반환하는 템플릿 태그"""
    return f"{settings.MEDIA_URL}{path}"
